import mysql.connector
from mysql.connector import Error

host = "127.0.0.1"  
port = 3306         
database = "wallet_network"  
user = "root"           
password = ""       

try:
    connection = mysql.connector.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

    if connection.is_connected():
        print("Connected to the database")

except Error as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Connection closed")
