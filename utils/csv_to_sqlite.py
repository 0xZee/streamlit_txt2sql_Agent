import pandas as pd
import sqlite3

def csv_to_sqlite(csv_path, database_name, table_name):
    
    # Read CSV
    df = pd.read_csv(csv_path)
    
    # Connect to SQLite
    conn = sqlite3.connect(database_name)
    
    # Save to SQLite
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    conn.close()
    print(f"CSV {csv_path} Saved to : \nSqlite Database : {database_name} => Table : {table_name}")

# Usage example:
csv_to_sqlite("csv_data/it_ops.csv", 'sqlite_db/it_ops.db', 'it_ops_2024')
csv_to_sqlite("csv_data/tech_stocks.csv", 'sqlite_db/tech_stocks.db', 'stocks_2024')
