# 01_db_connection/db_connect.py

import mysql.connector
from mysql.connector import Error

def create_connection():
    """
    Create and return a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',       
            user='root',  
            password='abc123', 
            database='ecommerce_analytics2'
        )
        if connection.is_connected():
            print("✅ Successfully connected to the database")
            return connection
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None

# Test connection if running this file directly
if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()
        print("Connection closed")
