
from app.extensions import db
from app.models.student import Student
from app.models.course import Course

# Hilfsfunktion (Testdaten erstellen, Tabellen erstellen)
def create_test_data():
    db.drop_all() # dieser Befehl löscht alle vorhandenen Datenbankeintraege und Tabellen
    db.create_all()

    # Beispieldaten
    students_data = [
        {'name': 'Alice Wonderland', 'level': 'Beginner'},
        {'name': 'Bob Marley', 'level': 'Beginner'},
        {'name': 'Charlie Chaplin', 'level': 'Advanced'},
        {'name': 'Eva Green', 'level': 'Expert'}
    ]
    for student_data in students_data:
        student = Student(**student_data)
        db.session.add(student)

    # create an additional student and safe ref for later
    student_ref = Student(name='Mega Tron', level='HF')
    db.session.add(student_ref)

    courses = [
        {'title': 'CS101'},
        {'title': 'PHYS202'}
    ]
    for course_data in courses:
        course = Course(**course_data)
        db.session.add(course)

    # create an additional course and safe ref for later
    course_ref = Course(title='LPEC24')
    db.session.add(course_ref)
    student_ref.courses.append(course_ref)

    db.session.commit()