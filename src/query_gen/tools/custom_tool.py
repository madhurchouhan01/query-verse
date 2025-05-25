from typing import Type

from crewai.tools import BaseTool
from crewai.tools import tool
import pymysql
# __import__('pysqlite3')
# import sys
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
@tool("Query Executer")
def query_executer(sql_query: str) -> str:
    """Executes the given SQL query and returns the result as a plain string."""
    
    conn = pymysql.connect(
        # host="mysql.railway.internal",
        host="yamanote.proxy.rlwy.net",
        user="root",
        password="KTNumwwPKBsVBqLAcaqoNdMgBzXpLnnG",
        database="railway",
        port=26984,
        cursorclass=pymysql.cursors.Cursor  
    )
    cursor = conn.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        return str(result)
    except Exception as e:
        return f"Error executing query: {e}"
    finally:
        cursor.close()
        conn.close()


@tool("IDU Query Executer")
def idu_query_executer(sql_query: str) -> str:
    """Executes the given Insertion, Deletion, or Updation SQL query and returns the result as a plain string."""

    conn = pymysql.connect(
        # host="mysql.railway.internal",
        host="yamanote.proxy.rlwy.net",
        user="root",
        password="KTNumwwPKBsVBqLAcaqoNdMgBzXpLnnG",
        database="railway",
        port=26984,
        cursorclass=pymysql.cursors.Cursor  
    )
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql_query)
        
        conn.commit()
        
        if sql_query.strip().upper().startswith("INSERT"):
            return "Insertion successful!"
        
        elif sql_query.strip().upper().startswith("DELETE"):
            rows_affected = cursor.rowcount
            return f"{rows_affected} row(s) deleted."
        
        elif sql_query.strip().upper().startswith("UPDATE"):
            rows_affected = cursor.rowcount
            return f"{rows_affected} row(s) updated."
        
        else:
            return "Query executed successfully, but no action needed for this type."
        
    except Exception as e:
        return f"Error executing query: {e}"
    
    finally:
        cursor.close()
        conn.close()
