from flask import Flask
import mysql.connector

app = Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mouli',
    'database': 'mydb'
}

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Database connection successful.")
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")

if __name__ == '__main__':
    app.run(debug=True)
