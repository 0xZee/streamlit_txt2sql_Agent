import streamlit as st
from sql_engine import SQLEngine
import pandas as pd

st.set_page_config(
    page_icon="✨",
    page_title="SQL ChatBot",
    layout="wide",
    initial_sidebar_state="auto"
)

def initialize_session_state():
    if "chat_started" not in st.session_state:
        st.session_state.chat_started = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sql_engine" not in st.session_state:
        st.session_state.sql_engine = SQLEngine(st.secrets["GROQ_API"])

initialize_session_state()

with st.sidebar:
    st.subheader("🅞🆇 Z 🅴🅴", divider="gray")
    st.write('TEXT-2-SQL Agent : `LangGraph, QuerySQLDatabaseTool & groq_inference : mixtral/llama3.2 llm`.')
    
    selected_db = st.selectbox(
        "📑Select Database",
        options=["tech_stocks", "it_ops"],
        key="db_select"
    )
    
    thread_id = st.text_input("🪟 Chat Session ID", value="001", key="thread_id")
    
    if not st.session_state.chat_started:
        if st.button("Start Chat Session", use_container_width=True):
            st.session_state.chat_started = True
            st.session_state.messages = []
            st.rerun()
    else:
        if st.button("End Chat Session", use_container_width=True, type="primary"):
            st.session_state.chat_started = False
            st.rerun()
    
    with st.expander("ℹ️ Example Questions", expanded=False):
        if selected_db == "tech_stocks":
            examples = [
                "Show me the stocks with market cap over 3T $",
                "Which stocks have the highest PE ratio?",
                "List companies in the Software sector"
            ]
        else:
            examples = [
                "Show all operations leaded by '0x Zee'.",
                "List the success ratio of operations leaded by 'John Doe'"
                "What's the average resolution time?",
            ]
        for example in examples:
            st.code(f"{example}")

st.subheader("၊၊||၊ :blue[TXT-2-SQL] 🅱🅞🆃 ☰ 📄", divider="green")

if st.session_state.chat_started:
    if not st.session_state.messages:
        welcome_msg = f"👋 Hi! I'm ready to help you query the `{selected_db}` database. What would you like to know?"
        st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "query" in message:
                st.code(message["query"], language="sql")
            if "result" in message:
                try:
                    df = pd.read_json(message["result"])
                    st.dataframe(df)
                except:
                    st.write("No data returned")

    if prompt := st.chat_input("Ask about your data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.sql_engine.chat(
                        prompt,
                        selected_db,
                        thread_id
                    )
                    
                    # Check for errors in response
                    if "error" in response["write_query"]:
                        st.error(response["write_query"]["error"])
                    elif "error" in response["execute_query"]:
                        st.markdown(response["execute_query"]["error"])
                    else:
                        st.markdown(response["generate_answer"]["answer"])
                        with st.expander("▶️ Requête - Query") :
                            st.code(response["write_query"]["query"], language="sql")
                        with st.expander("🔢 Données Sources - Raw Data") :
                                    st.code(response["execute_query"]["result"])
                        
                        # Handle dataframe display
                        #if response["execute_query"]["result"] != "[]":
                        #    try:
                                #with st.expander("📑💎🪟#️⃣▶️🔢⏹️⏹️➡️ℹ️🔄🔣↘️⏺️↗️*️⃣⏹ ➕☑️☑️✖️🆔 Données Sources - Raw Data") :
                        #        with st.expander("🔢 Données Sources - Raw Data") :
                        #            st.code(response["execute_query"]["result"])
                                #df = pd.read_json(response["execute_query"]["result"])
                                #if not df.empty:
                                #    st.dataframe(df)
                                #else:
                                #    st.info("Query returned no results.")
                        #    except:
                        #        st.warning("Could not parse results into table format.")
                        #else:
                        #    st.info("No data returned for this query.")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response.get("generate_answer", {}).get("answer", ""),
                        "query": response["write_query"].get("query", ""),
                        "result": response["execute_query"].get("result", "[]")
                    })
                except Exception as e:
                    error_msg = "Something went wrong. Please try rephrasing your question."
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })
else:
    st.write("Chat with your databases using natural language.")
    st.write("Available Databases : `tech_stocks` ; `it_ops` .")
