import pytest
from website import create_app, db
from website.models import User
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


@pytest.fixture()
def app():
    app = create_app()

    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def test_sign_up_success(client):
    response = client.post('/sign-up', data={
        'email': 'test@example.com',
        'firstName': 'John',
        'password1': 'password123',
        'password2': 'password123',
        'role': 'candidate'
    }, follow_redirects=True)

    assert response.status_code == 200

def test_sign_up_existing_email(client):
    response = client.post('/sign-up', data={
        'email': 'test@example.com',
        'firstName': 'John',
        'password1': 'password123',
        'password2': 'password123',
        'role': 'candidate'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Email already exists.' in response.data

def test_login_success(client):
    with client:
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Logged in successfully!' in response.data

def test_login_incorrect_password(client):
    with client:
        response = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Incorrect password, try again.' in response.data
        

def test_login_email_not_exist(client):
    with client:
        response = client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'password123'
        }, follow_redirects=True)

        assert response.status_code == 200
        assert b'Email does not exist.' in response.data



def test_cv_success(client):
    response = client.post('/cv', data={
        'ProgrammingLanguage': 'Python',
        'EngineeringSkill': 'Mechanical Engineering',
        'ITSkill': 'Network Administration',
        'ManagementSkill': 'Project Management',
        'MarketingSkill': 'Digital Marketing',
    }, follow_redirects=True)

    print(response.status_code)
    print(response.data)

    assert response.status_code == 200


def test_home_success(client):
    with client:
        with client.session_transaction() as session:
            session['role'] = 'admin'

        response = client.post('/', data={
            'title': 'Test Note',
            'note': 'This is a test note.'
        }, follow_redirects=True)

        assert response.status_code == 200



def test_create_test_success(client):
    with client:
        with client.session_transaction() as session:
            session['role'] = 'admin'

        client.post('/create_test', data={
            'test_name': 'Sample Test',
            'question_count': '2',
            'question_1': 'Question 1',
            'option1_1': 'Option 1.1',
            'option2_1': 'Option 1.2',
            'option3_1': 'Option 1.3',
            'option4_1': 'Option 1.4',
            'correct_answer_1': 'Option 1.3',
            'question_2': 'Question 2',
            'option1_2': 'Option 2.1',
            'option2_2': 'Option 2.2',
            'option3_2': 'Option 2.3',
            'option4_2': 'Option 2.4',
            'correct_answer_2': 'Option 2.2'
        })


        response = client.get('/create_test')

        print(response.status_code)
        print(response.data)

        assert response.status_code == 302