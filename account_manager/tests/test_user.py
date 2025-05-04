import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestUserRegistration:
    def test_user_registration(self, api_client, user_data):
        url = reverse('rest_register')
        response = api_client.post(url, user_data)
        print("############### Register user ####", response.data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.count() == 1
        user = User.objects.first()
        assert user.email == user_data['email']
        assert user.role == user_data['role']

@pytest.mark.django_db
class TestUserAPI:
    def test_user_login(self, api_client, create_user, user_data):
        url = reverse('rest_login')
        response = api_client.post(url, {
            'email': user_data['email'],
            'password': user_data['password1']
        })
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
