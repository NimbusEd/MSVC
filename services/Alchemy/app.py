from apiflask import APIFlask, Schema
from apiflask.fields import Integer, String, Nested
from apiflask.validators import Length, OneOf
from flask_sqlalchemy import SQLAlchemy
import os

app = APIFlask(__name__)

# Connection string to mysql or local /app/app.db
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create object
db = SQLAlchemy(app)

# Relation for many-2-many
student_class_association = db.Table(
    'student_class',
    db.Column('student_id', db.Integer, db.ForeignKey('classes.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('student_model.id'))
)

# Set table for Class
class Class(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(8))
    students = db.relationship('StudentModel', secondary=student_class_association, back_populates='classes')

class ClassIn(Schema):
    title = String(required=True, validate=Length(0, 32))

class ClassOut(Schema):
    id = Integer()
    title = String()

# Set table for StudentModel
class StudentModel(db.Model):
    __tablename__ = 'student_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.String(32))
    classes = db.relationship('Class', secondary=student_class_association, back_populates='students')

class StudentIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    level = String(required=True, validate=OneOf(['Beginner', 'Intermediate', 'Advanced', 'Expert']))


class StudentOut(Schema):
    id = Integer()
    name = String()
    level = String()

class RegistrationIn(Schema):
    class_id = Integer()

# Add example data
    
def example_database():
    db.drop_all()
    db.create_all()

    # Sample data
    students_data = [
        {'name': 'Alice Wonderland', 'level': 'Beginner'},
        {'name': 'Bob Marley', 'level': 'Intermediate'},
        {'name': 'Charlie Chaplin', 'level': 'Advanced'},
        {'name': 'Eva Green', 'level': 'Expert'}
    ]
    students = [StudentModel(**data) for data in students_data]
    db.session.add_all(students)

    class_data = [
        {'title': 'CS101'},
        {'title': 'PHYS202'}
    ]
    classes = [Class(**data) for data in class_data]
    db.session.add_all(classes)
    db.session.commit()


@app.get('/')
def say_hello():
    db_file_path = os.path.join(basedir, 'app.db')
    return {'message': f'Hi this is a Flask App'}

# Get method student by ID
@app.get('/students/<int:student_id>')
@app.output(StudentOut)
def get_student(student_id):
    return db.get_or_404(StudentModel, student_id)


# Get method all students
@app.get('/students')
@app.output(StudentOut(many=True))
def get_students():
    return StudentModel.query.all()

# Post method create new student
@app.post('/students')
@app.input(StudentIn, location='json')
@app.output(StudentOut, status_code=201)
def create_student(json_data):
    student = StudentModel(**json_data)
    db.session.add(student)
    db.session.commit()
    return student

# Patch method update student
@app.patch('/students/<int:student_id>')
@app.input(StudentIn(partial=True), location='json')
@app.output(StudentOut)
def update_student(student_id, json_data):
    student = db.get_or_404(StudentModel, student_id)
    for attr, value in json_data.items():
        setattr(student, attr, value)
    db.session.commit()
    return student

# Delete method remove student
@app.delete('/students/<int:student_id>')
@app.output({}, status_code=204)
def delete_student(student_id):
    student = db.get_or_404(StudentModel, student_id)
    db.session.delete(student)
    db.session.commit()
    return ''

# Post mehtod add student to class
@app.post('/students/<int:student_id>/courses')
@app.input(RegistrationIn, location='json')
@app.output(StudentOut, status_code=201)
def register_student(student_id, json_data):
    student = db.get_or_404(StudentModel, student_id)
    classs = db.get_or_404(Class, json_data.get('class_id'))
    student.classes.append(classs)
    classs.students.append(student)
    db.session.commit()
    return student

# Get method see all classes of student
@app.get('/students/<int:student_id>/courses')
@app.output(ClassOut(many=True))
def get_student_courses(student_id):
    student = db.get_or_404(StudentModel, student_id)
    classes = student.classes
    return classes


with app.app_context():
    db.create_all()
    example_database()
