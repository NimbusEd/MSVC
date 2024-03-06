from apiflask import APIFlask, Schema
from apiflask.fields import Integer, String, Nested
from apiflask.validators import Length, OneOf
from flask_sqlalchemy import SQLAlchemy
import os

app = APIFlask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'app.db')


db = SQLAlchemy(app)

class StudentModel(db.Model):
    __tablename__ = 'student_model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.String(8))

class StudentIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    level = String(required=True, validate=OneOf(['HF', 'PE', 'AP', 'ICT']))


class StudentOut(Schema):
    id = Integer()
    name = String()
    level = String()


@app.get('/')
def say_hello():
    db_file_path = os.path.join(basedir, 'app.db')
    return {'message': f'Absolute path of the app.db file: {db_file_path}'}

@app.get('/students')
@app.output(StudentOut(many=True))
def get_students():
    return StudentModel.query.all()


@app.post('/students')
@app.input(StudentIn, location='json')
@app.output(StudentOut, status_code=201)
def create_student(json_data):
    student = StudentModel(**json_data)
    db.session.add(student)
    db.session.commit()
    return student



with app.app_context():
    db.create_all()
