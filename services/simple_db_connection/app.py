import requests
from flask import jsonify, request
from apiflask import APIFlask, Schema
from apiflask.fields import Float, Integer, String
import mysql.connector
from database import create_tables, list_employees_from_db, create_employee

app = APIFlask(__name__, docs_ui='swagger-ui')


@app.route('/')
def hello_world():
    return 'Hello ITCNE!'


# Route to list employees
@app.route('/ListEmployees')
def list_employees():
    # Call create_tables to ensure the table exists
    create_tables()

    # Call list_employees_from_db to get the list of employees
    employees = list_employees_from_db()

    return jsonify(employees)


class Input(Schema):
    first_name = String(required=True)
    last_name = String(required=True)


# Route to create a new employee
@app.route('/CreateEmployee', methods=['POST'])
@app.input(Input, location='json')  # Change location to 'json'
def create_employee_route(json_data):  # Change argument name to match decorator
    # Call create_tables to ensure the table exists
    create_tables()

    # Get data from the decorator-provided argument
    data = json_data

    if 'last_name' not in data or 'first_name' not in data:
        return jsonify({'error': 'Missing last name or first name'}), 400

    last_name = data['last_name']
    first_name = data['first_name']

    result = create_employee(last_name, first_name)

    return jsonify(result)



# Initialize the application
if __name__ == '__main__':
    app.run()
