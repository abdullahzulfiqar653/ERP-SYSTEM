from rest_framework import status
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from .models import UserTableDB


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

'''Here we are overriding JSONWEBTokenSerializer because we want our users to login with email
and username both also here in response we are adding is_admin so on client side it will be
evaluated if the user is admin or a normal user'''
class CustomJWTSerializer(JSONWebTokenSerializer):               
    username_field = 'username_or_email'
    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("username_or_email")).first() or User.objects.filter(username=attrs.get("username_or_email")).first()
        if user_obj is not None:
            credentials = {
                'username':user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)
                    payload = jwt_payload_handler(user)
                    return {
                        'token': jwt_encode_handler(payload),
                        'is_admin': user.is_superuser,
                        'email': user.email
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)
        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)


'''This Serializer validating password with build in method validate password and
in valdate method checking if both entered passwords are same. Also verfying
uniqueness of email requested to register. if is_valid() comes true then creating
a user and also an profile for that user. Note:profile model name is UserTableDB'''
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, validators=[validate_password])
    password1 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'password1',
        ]
    def validate(self, attrs):
        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "password fields did not match."})
        return attrs
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

'''This Change passswrod serialzer checking if new passwords are matched
and if not matched then generating validation Error'''
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password1']:
            raise serializers.ValidationError({"password": "password fields did not match."})
        return attrs

# This serialzer is for the view where admin changing the password of a company without putting old password.
class AdminChangeCompanyPasswordSerializer(serializers.Serializer):
    model = User
    company_id = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password1 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password1']:
            raise serializers.ValidationError({"password": "password fields did not match."})
        if not attrs['company_id']:
            raise serializers.ValidationError({'company_id': "company id required."})
        return attrs

class FetchUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
        ]

'''Serializer to return only id and username fields as needed for frontend'''
class CompaniesFetchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]

