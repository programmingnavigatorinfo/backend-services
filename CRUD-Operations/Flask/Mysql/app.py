from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mouli',
    'database': 'mydb'
}

# Establish Database Connection
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Database connection successful.")
except mysql.connector.Error as err:
    print(f"Database connection failed: {err}")



@app.route("/employees", methods=['GET'])
def get_employees():
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM USERS")
        records = cursor.fetchall()
        return jsonify(records), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# READ Operation: Fetch an employee by ID
@app.route("/employees/<int:id>", methods=['GET'])
def get_employee_by_id(id):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM USERS WHERE id = %s"
        cursor.execute(query, (id,))
        record = cursor.fetchone()
        if not record:
            return jsonify({'message': 'Employee not found.'}), 404
        return jsonify(record), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# CREATE Operation: Add a new employee
@app.route("/employees", methods=['POST'])
def add_employee():
    data = request.json
    try:
        # Password hashing for security
        #hashed_password = generate_password_hash(data['password'], method='sha256')
        
        cursor = connection.cursor()
        query = "INSERT INTO USERS (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (data['name'], data['email'], data['password']))
        connection.commit()
        return jsonify({'message': 'Employee added successfully!'}), 201
    except mysql.connector.IntegrityError as e:
        return jsonify({'error': 'Email must be unique.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# UPDATE Operation: Update an employee's details
@app.route("/employees/<int:id>", methods=['PUT'])
def update_employee(id):
    data = request.json
    try:
        cursor = connection.cursor()
        query = """
            UPDATE USERS 
            SET name = %s, email = %s, password = %s 
            WHERE id = %s
        """
        # hashed_password = generate_password_hash(data['password'], method='sha256')
        cursor.execute(query, (data['name'], data['email'], data['password'], id))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Employee not found.'}), 404
        return jsonify({'message': 'Employee updated successfully!'}), 200
    except mysql.connector.IntegrityError as e:
        return jsonify({'error': 'Email must be unique.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


# DELETE Operation: Delete an employee
@app.route("/employees/<int:id>", methods=['DELETE'])
def delete_employee(id):
    try:
        cursor = connection.cursor()
        query = "DELETE FROM USERS WHERE id = %s"
        cursor.execute(query, (id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'Employee not found.'}), 404
        return jsonify({'message': 'Employee deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()


if __name__ == '__main__':
    app.run(debug=True)