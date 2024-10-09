from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database connection function
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='newsfeed_db',
            user='your_username',
            password='your_password'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)