from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.mark.django_db
class TestUser:
    def test_admin_create_return_201(self):
        # Arrange
        # Act
        client = APIClient()
        response = client.post('/api/core/admin/register/', {
            'email': 'someone@example.com',
            'username': 'someone example',
            'password': 'haha@123'
        })

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] is not None

    def test_if_admin_create_payload_is_invalid_return_400(self):
        # Arrange
        # Act
        client = APIClient()
        response = client.post('/api/core/admin/register/', {
            'email': '',
            'username': '',
            'password': ''
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'] is not None
        assert response.data['username'] is not None
        assert response.data['password'] is not None

    def test_subuser_create_if_current_user_is_not_admin_return_401(self):
        # Arrange

        # Act
        client = APIClient()
        # client = client.force_authenticate(user={})
        response = client.post('/api/core/user/register/', {
            'email': 'someone@example.com',
            'username': 'someone example',
            'password': 'haha@123'
        })
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # @pytest.mark.skip
    def test_subuser_create_if_current_user_is_admin_return_201(self):
        # Arrange
        user = baker.make(User, is_staff=True)
        # Act
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/api/core/user/register/', {
            'email': 'sample@admin.com',
            'username': 'someone example',
            'password': 'haha@123'
        })
        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_subuser_create_payload_is_invalid_return_400(self):
        # Arrange
        user = baker.make(User, is_staff=True)
        # Act
        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post('/api/core/user/register/', {
            'email': '',
            'username': '',
            'password': ''
        })

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'] is not None
        assert response.data['username'] is not None
        assert response.data['password'] is not None

    def test_admin_or_subuser_login_return_200(self):
        client = APIClient()
        user = baker.make(User, email='someone@gmail.com')
        user.set_password("haha@123")
        user.save()
        user.user_profile.isactive = True
        user.user_profile.save()
        response = client.post('/api/core/login/', {
            "email": "someone@gmail.com",
            "password": "haha@123"
        })
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_admin_or_subuser_login_if_payload_invalid_return_400(self):
        client = APIClient()
        response = client.post('/api/core/login/', {
            "email": "",
            "password": "haha@123"
        })
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inactive_admin_or_subuser_login_return_406(self):
        client = APIClient()
        user = baker.make(User, email='someone@gmail.com')
        user.set_password("haha@123")
        user.save()
        response = client.post('/api/core/login/', {
            "email": "someone@gmail.com",
            "password": "haha@123"
        })
        # Assert
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    @pytest.mark.skip
    def test_admin_or_subuser_if_valid_token_return_200(self):
        # Arrange
        user = baker.make(User, email='someone@gmail.com')
        user.set_password("haha@123")
        user.save()
        user.user_profile.isactive = True
        user.user_profile.save()
        # Act
        client = APIClient()
        print(client.login(user=user.username, password="haha@123"))

        response = client.post('/api/core/login/', {
            "email": "someone@gmail.com",
            "password": "haha@123"
        })
        print(response.data)
        response = client.get('/api/core/auth/user/', {
            "email": "someone@gmail.com",
            "password": "haha@123"
        })
        print(response)
        # Assert
        assert response.status_code == status.HTTP_200_OK
