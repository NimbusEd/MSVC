from apiflask import Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf

from app.extensions import db
from app.models.registration import Registration

class StudentIn(Schema):
    name = String(required=True, validate=Length(0, 32))
    level = String(required=True, validate=OneOf(['Beginner', 'Intermediate', 'Advanced', 'Expert']))
    email = String()

class StudentOut(Schema):
    id = Integer()
    name = String()
    level = String()
    email = String()

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    level = db.Column(db.String(8))
    email = db.Column(db.String(244))
    courses = db.relationship('Course', secondary='registrations', back_populates='students')