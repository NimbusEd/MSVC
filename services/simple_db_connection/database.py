import sqlite3
import mysql.connector


def set_connection():
    return mysql.connector.connect(
        host='mysql',
        port=3306,
        user='root',
        password='password',
        database='employees'
    )

def create_tables():
    conn = set_connection()
    cursor = conn.cursor()
    c = conn.cursor()

    # Create Employee table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS employee (
             id INTEGER PRIMARY KEY AUTO_INCREMENT,
             last_name TEXT,
             first_name TEXT
             )''')

    conn.commit()
    conn.close()


def list_employees_from_db():
    conn = set_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM employee')
    employees = cursor.fetchall()

    conn.close()

    return employees


def create_employee(last_name, first_name):
    conn = set_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO employee (last_name, first_name) VALUES (%s, %s)', (last_name, first_name))

    conn.commit()
    conn.close()

    return {'message': 'Employee created successfully'}