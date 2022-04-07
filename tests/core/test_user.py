from asyncio.windows_events import NULL
from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture
def register_admin_user(api_client):
    def do_register_admin_user(data):
        response = api_client.post('/api/core/admin/register/', data)
        return response
    return do_register_admin_user


@pytest.fixture
def create_user(api_client):
    def do_get_user(data, isactive=False, is_staff=False):
        user = baker.make(User, email=data['email'], is_staff=is_staff)
        user.set_password(data['password'])
        user.save()
        user.user_profile.isactive = isactive
        user.user_profile.save()
        # Act
        response = api_client.post('/api/core/login/', {
            "email": data['email'],
            "password": data['password']
        })
        return response
    return do_get_user


@pytest.fixture
def register_subuser(api_client):
    def do_register_subuser(data, headers):
        response = api_client.post('/api/core/user/register/', data, **headers)
        return response
    return do_register_subuser


@pytest.fixture
def email_verify(api_client):
    def do_email_verify(data):
        user = baker.make(User, email=data["email"])
        user.user_profile.activation_key = data["key"]
        user.user_profile.is_activation_key_used = data["status"]
        user.user_profile.save()
        # Act
        response = api_client.post(
            '/api/core/email/activate/',
            {"activation_key": "" if data["key"] == NULL else user.user_profile.activation_key})
        return response
    return do_email_verify

# ---------------------------------------------------------------------------------------------- #
# ------------------------------------User Model Test Cases------------------------------------- #
# ---------------------------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestUser:

    # ----------------------------Admin register Endpoint Test Cases---------------------------- #
    def test_admin_create_return_201(self, register_admin_user):
        # Arrange
        response = register_admin_user({
            'email': 'someone@example.com',
            'username': 'someone example',
            'password': 'haha@123'
        })
        # Act
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] is not None

    def test_if_admin_create_payload_is_invalid_return_400(self, register_admin_user):
        # Arrange
        response = register_admin_user({
            'email': '',
            'username': '',
            'password': ''
        })
        # Act
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'] is not None
        assert response.data['username'] is not None
        assert response.data['password'] is not None

    # ----------------------------Subuser register Endpoint Test Cases---------------------------- #
    def test_subuser_create_if_current_user_is_not_admin_return_401(self, register_subuser):
        # Arrange
        # Act
        headers = {'HTTP_AUTHORIZATION': "JWT dfgsfsf"}
        response = register_subuser({
            'email': 'someone@example.com',
            'username': 'someone example',
            'password': 'haha@123'
        }, headers)
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_subuser_create_if_current_user_is_admin_return_201(self, register_subuser, create_user):
        # Arrange
        response = create_user({
            "email": "someone@gmail.com",
            "password": "haha@123",
        }, True, True)
        headers = {'HTTP_AUTHORIZATION': "JWT {}".format(response.data['token'])}
        # Act
        response = register_subuser({
            'email': 'sample@admin.com',
            'username': 'someone example',
            'password': 'haha@123'
        }, headers)
        # Assert
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_subuser_create_payload_is_invalid_return_400(self, register_subuser, create_user):
        # Arrange
        response = create_user({
            "email": "someone@gmail.com",
            "password": "haha@123",
        }, True, True)
        headers = {'HTTP_AUTHORIZATION': "JWT {}".format(response.data['token'])}
        # Act
        response = register_subuser({
            'email': '',
            'username': '',
            'password': ''
        }, headers)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['email'] is not None
        assert response.data['username'] is not None
        assert response.data['password'] is not None

    # ----------------------------Email verification Endpoint Test Cases---------------------------- #
    def test_email_verify_token_if_not_exist_return_400(self, email_verify):
        response = email_verify({
            "email": "someone@example.com",
            "key": NULL,
            "status": False
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_email_verify_token_if_expired_return_403(self, email_verify):
        response = email_verify({
            "email": "someone@example.com",
            "key": "ahcxwkea",
            "status": True
        })
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_email_verify_token_if_Accepted_return_202(self, email_verify):
        response = email_verify({
            "email": "someone@example.com",
            "key": "ahcxwkea",
            "status": False
        })
        assert response.status_code == status.HTTP_202_ACCEPTED

    # ----------------------------Login Endpoint Test Cases---------------------------- #
    def test_admin_or_subuser_login_return_200(self, create_user):
        response = create_user({
            "email": "someone@gmail.com",
            "password": "haha@123",
        }, True)
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_admin_or_subuser_login_if_payload_invalid_return_400(self, create_user):
        response = create_user({
            "email": "",
            "password": "haha@123",
        })
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_inactive_admin_or_subuser_login_return_406(self, create_user):
        response = create_user({
            "email": "someone@gmail.com",
            "password": "haha@123",
        })
        assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE

    # ----------------------------refresh token Endpoint Test Cases---------------------------- #
    def test_admin_or_subuser_if_valid_token_return_200(self, api_client, create_user):
        # Arrange
        # Act
        response = create_user({
            "email": "someone@gmail.com",
            "password": "haha@123",
        }, True)
        headers = {'HTTP_AUTHORIZATION': "JWT {}".format(response.data['token'])}
        response = api_client.get('/api/core/auth/user/', **headers)
        # Assert
        assert response.status_code == status.HTTP_200_OK

    def test_admin_or_subuser_if_token_invalid_return_401(self, api_client):
        # Arrange
        # Act
        headers = {'HTTP_AUTHORIZATION': "JWT akhdkadkaxa"}
        response = api_client.get('/api/core/auth/user/', **headers)
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
