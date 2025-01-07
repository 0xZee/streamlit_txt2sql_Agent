from typing import Dict, Any
from typing_extensions import TypedDict, Annotated
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st

class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

class QueryOutput(TypedDict):
    query: Annotated[str, "Syntactically valid SQLite query."]

class SQLEngine:
    def __init__(self, api_key: str):
        self.llm = ChatGroq(
            temperature=0.1,
            groq_api_key=st.secrets["GROQ_API"],
            #model_name="llama-3.2-3b-preview"
            #model_name="gemma2-9b-it"
            model_name="mixtral-8x7b-32768"
        )
        self.setup_databases()
        self.setup_prompts()
        
    def setup_databases(self):
        self.dbs = {
            'tech_stocks': SQLDatabase.from_uri("sqlite:///sqlite_db/tech_stocks.db"),
            'it_ops': SQLDatabase.from_uri("sqlite:///sqlite_db/it_ops.db")
        }
        
    def setup_prompts(self):
        self.query_prompt = ChatPromptTemplate.from_messages([
            ("system",  "You are an SQL expert. Generate a {dialect} query to answer the user's question.\n\n"
                        "Unless the user specifies in his question a specific number of examples they wish to obtain, always limit your query to at most {top_k} results. You can order the results by a relevant column to return the most interesting examples in the database.\n"
                        "Never query for all the columns from a specific table, only ask for a the few relevant columns given the question.\n"
                        "Pay attention to use only the column names that you can see in the schema description. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.\n\n"
                        "Only use the following table : {table_info}\n\n"
                        "Return only the SQL query without any explanation, without triple quote ```."),
            ("human",   "{input}")
        ])
        
    def write_query(self, state: State, db_name: str) -> Dict[str, str]:
        try:
            prompt = self.query_prompt.invoke({
                "dialect": self.dbs[db_name].dialect,
                "top_k": 15,
                "table_info": self.dbs[db_name].get_table_info(),
                "input": state["question"]
            })
            structured_llm = self.llm.with_structured_output(QueryOutput)
            result = structured_llm.invoke(prompt)
            return {"query": result["query"]}
        except Exception as e:
            return {"query": "ERROR", 
                    "error": "I cannot understand how to query this. Please reformulate your question."}
        
    def execute_query(self, state: State, db_name: str) -> Dict[str, str]:
        try:
            if state.get("query") == "ERROR":
                return {"result": "[]", "error": state.get("error")}
            execute_query_tool = QuerySQLDatabaseTool(db=self.dbs[db_name])
            result = execute_query_tool.invoke(state["query"])
            # Ensure result is valid JSON array
            if not result.startswith("["):
                result = f"[{result}]"
            return {"result": result}
        except Exception as e:
            return {"result": "[]", 
                    "error": "Unable to execute query. Please try a different question."}
        
    def generate_answer(self, state: State) -> Dict[str, str]:
        prompt = (
            "Given the following user question, SQL query, and result, provide a clear answer.\n\n"
            f"Question: {state['question']}\n"
            f"SQL Query: {state['query']}\n"
            f"SQL Result: {state['result']}\n\n"
            "Answer and Format below any data as a markdown table when appropriate."
        )
        response = self.llm.invoke(prompt)
        return {"answer": response.content}
    
    def create_graph(self, db_name: str):
        def write_query_with_db(state): 
            return self.write_query(state, db_name)
        def execute_query_with_db(state): 
            return self.execute_query(state, db_name)
            
        workflow = StateGraph(State)
        workflow.add_node("write_query", write_query_with_db)
        workflow.add_node("execute_query", execute_query_with_db)
        workflow.add_node("generate_answer", self.generate_answer)
        
        workflow.add_edge(START, "write_query")
        workflow.add_edge("write_query", "execute_query")
        workflow.add_edge("execute_query", "generate_answer")
        
        return workflow.compile()
    
    def chat(self, question: str, db_name: str, thread_id: str) -> Dict[str, Any]:
        graph = self.create_graph(db_name)
        memory = MemorySaver()
        
        results = {}
        for step in graph.stream(
            {"question": question},
            config={"configurable": {"thread_id": thread_id}}
        ):
            results.update(step)
            
        return results
