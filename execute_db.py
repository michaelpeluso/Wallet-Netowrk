import os
import mysql.connector
from mysql.connector import Error

# create db connection
def get_db_connection():
    try: 
        connection = mysql.connector.connect(host="10.192.146.79", port=3306, database="wallet_network", user="user")

        if connection.is_connected():
            print("Database connection successful")
            return connection
        
    except Error as e:
        print(f"Error: {e}")
        return None
    
def execute_query(query, params=None):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error executing query: {e}")
        finally:
            cursor.close()
            connection.close()
            print("Connection closed")

def fetch_query(query, params=None):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
            print("Connection closed")


# print(execute_query("INSERT INTO bank_account (BankID, BANumber) VALUES (%s, %s)", (5, '312985671')))

insert_wallet = """
                INSERT INTO WALLET_ACCOUNT (SSN, Name, PhoneNo, Balance, BankID, BANumber, BAVerified)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """

execute_query(insert_wallet, (123456789, 'Michael Peluso', '9731231234', 0.00, None, None, False))