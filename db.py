import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="10.203.3.88",
            port=3306,
            database="wallet_network",
            user="user"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(str(e), 'danger')
        raise Exception(f"Database connection error: {str(e)}")

def execute_query(q, p=None):
    conn = get_db_connection()
    if not conn:
        raise Exception("No database connection")
    try:
        c = conn.cursor()
        c.execute(q, p)
        conn.commit()
        print("Query executed successfully")
    except Error as e:
        print(str(e), 'danger')
        raise Exception(f"Database error: {str(e)}")
    finally:
        c.close()
        conn.close()

def fetch_query(q, p=None):
    conn = get_db_connection()
    if not conn:
        raise Exception("No database connection")
    try:
        c = conn.cursor(dictionary=True)
        c.execute(q, p)
        print("Query executed successfully")
        return c.fetchall()
    except Error as e:
        print(str(e), 'danger')
        raise Exception(f"Database error: {str(e)}")
    finally:
        c.close()
        conn.close()
