from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus
from datetime import datetime
from bson import ObjectId

app = Flask(__name__)

# MongoDB Configuration
username = "programmingnavigatorinfo"
password = "ProgrammingNavigator@1234"

encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

mongo_url = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.2hthl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Establish MongoDB Connection
try:
    client = MongoClient(mongo_url)
    db = client.BACKEND_PORTFOLIO  # Database
    employee_collection = db.EMPLOYEE  # Collection
    client.admin.command('ping')
    print("MongoDB connection successful.")
except ConnectionFailure as err:
    print(f"MongoDB connection failed: {err}")

# Helper Function to Convert ObjectId to String
def serialize_employee(employee):
    employee['_id'] = str(employee['_id'])
    return employee


# READ Operation: Fetch all employees
@app.route("/employees", methods=['GET'])
def get_employees():
    try:
        employees = list(employee_collection.find())
        return jsonify([serialize_employee(emp) for emp in employees]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ Operation: Fetch an employee by ID
@app.route("/employees/<string:id>", methods=['GET'])
def get_employee_by_id(id):
    try:
        employee = employee_collection.find_one({'_id': ObjectId(id)})
        if not employee:
            return jsonify({'message': 'Employee not found.'}), 404
        return jsonify(serialize_employee(employee)), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# CREATE Operation: Add a new employee
@app.route("/employees", methods=['POST'])
def add_employee():
    data = request.json
    try:
        new_employee = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password'],  # Consider hashing for security
            'created_at': datetime.utcnow()
        }
        result = employee_collection.insert_one(new_employee)
        return jsonify({'message': 'Employee added successfully!', 'id': str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# UPDATE Operation: Update an employee's details
@app.route("/employees/<string:id>", methods=['`PUT`'])
def update_employee(id):
    data = request.json
    try:
        update_data = {
            'name': data.get('name'),
            'email': data.get('email'),
            'password': data.get('password'),  # Consider hashing for security
        }
        result = employee_collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': update_data}
        )
        if result.matched_count == 0:
            return jsonify({'message': 'Employee not found.'}), 404
        return jsonify({'message': 'Employee updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# DELETE Operation: Delete an employee
@app.route("/employees/<string:id>", methods=['DELETE'])
def delete_employee(id):
    try:
        result = employee_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({'message': 'Employee not found.'}), 404
        return jsonify({'message': 'Employee deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)