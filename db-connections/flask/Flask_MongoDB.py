from flask import Flask
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus


app = Flask(__name__)

username = "programmingnavigatorinfo"
password = "ProgrammingNavigator@1234"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

mongo_url=f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.2hthl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(mongo_url)
    db = client.BACKEND_PORTFOLIO
    client.admin.command('ping')
    print("MongoDB connection successful.")
except ConnectionFailure as err:
    print(f"MongoDB connection failed: {err}")

if __name__ == '__main__':
    app.run(debug=True)
