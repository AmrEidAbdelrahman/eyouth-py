import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user_data():
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'testpass123',
        'password2': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User',
        'role': 'STUDENT'
    }

@pytest.fixture
def create_user(user_data):
    return User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password1'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        role=user_data['role']
    ) 
