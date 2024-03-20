from test import client

def test_get_students(client):
    response = client.get("/studiis/")
    assert response.json[4]['name'] == 'Mega Tron'

def test_get_student(client):
    response = client.get("/studiis/2")
    assert response.json["name"] == "Bob Marley"

def test_post_student(client):
    response = client.post("/studiis/", json={
            'name': 'Nina Hagen', 'level': 'Beginner'
        })
    assert response.status_code == 201

def test_change_student(client):
    response = client.patch("/studiis/2", json={'level': 'Beginner'})
    assert response.json['level'] == 'Beginner'

def test_register_student(client):
    response = client.post("/studiis/2/courses", json={'course_id': '1'})
    assert response.status_code == 201

def test_get_student_courses(client):
    response = client.get("/studiis/5/courses")
    assert response.json[0]['title'] == 'LPEC24'
