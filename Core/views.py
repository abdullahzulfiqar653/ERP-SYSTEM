from django.conf import settings
from rest_framework import serializers
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from utils.pagination import CompaniesLimitOffsetPagination
from utils.email import send_email
from .models import UserTableDB
from.helper import generate_token
from .serializers import (
        RegisterSerializer,
        ChangePasswordSerializer,
        CustomJWTSerializer,
        CompaniesFetchSerializer,
        FetchUserProfileSerializer,
        AdminChangeCompanyPasswordSerializer
    )


'''Here we are customizing ObtainJSONWebToken View to return one more attribute is_admin so in client side 
developer can check the user logged in is an admin user or a simple user.'''
class CustomJWTView(ObtainJSONWebToken):
    serializer_class=CustomJWTSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({
                'token': serializer.validated_data['token'],
                'is_admin': serializer.validated_data['is_admin'],
                'email': serializer.validated_data['email']
            }, status.HTTP_200_OK)
        else:
            raise serializers.ValidationError({"fields_error":"Account with provided credentials does not exists"}, status.HTTP_400_BAD_REQUEST)


'''This View is for registration of users. A user can register his self bases on 4 arguments:
like email, username and a strong password and retyped password. This View check the validations
and if all 4 arguments are Correct then user will be registered and recieve an email of Welcome
and also a link attached so that he can verify his email through that link.'''
class RegisterAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, format='json'):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.validated_data['email'])
            email_activation_token = generate_token()
            # This is Content we need to send for email after registration process
            email = {
                "title": "Thank your for registering with BoosterTech Portal",
                "shortDescription": "These are the next steps.",
                "subtitle": "BoosterTech Business handling solution in one go",
                'link': settings.PASSWORD_RESET_PROTOCOL + '://'+ settings.PASSWORD_RESET_DOMAIN +'/api/core/email/activate/activation_key='+ email_activation_token,
                "message": '''You have successfully registered with BoosterTech. You can 
                        now login in to your profile and start. We have 
                        thousands of features just waiting for you to use. If you experience any 
                        issues feel free to contact our support at support@boostertech.com>'''
                    }
            subject = 'Welcome to Booster Tech'
            to_email = serializer.validated_data['email']
            send_email( email, subject, to_email, 'register.html')
            user.user_profile.activation_key = email_activation_token
            user.user_profile.is_activation_key_used = False
            user.user_profile.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''This view accepting post request and in the payload clientside will send an activation_key
after that this view checks if the key exists or not if exist then verify if it is already used
or a fresh key, if it is a fresh key then find the user against that key and  make that user active.'''
class UserEmailVerifyView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            if request.data['activation_key']:
                pass
        except:
            return Response(status=status.HTTP_205_RESET_CONTENT)
        activation_key = request.data['activation_key']
        if UserTableDB.objects.filter(activation_key=activation_key).exists():
            customer = UserTableDB.objects.get(activation_key=activation_key)
            if not customer.is_activation_key_used:
                customer.isactive = True
                customer.is_activation_key_used = True
                customer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


'''This view is for users who want to update their password. This View updating password for
admin or simple users except those who are not authenticated. This View first checking if
old password is rite then using serialzer validating the password and password1 if they
are matched then updating password.'''
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    # method returning object of current user.
    def get_object(self):
        return self.request.user

    # method updating password for authenticated user after serializing.
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Checking if the old password is correct or not
            print(self.object.check_password(serializer.data.get("old_password")), "aaaaaaaaaaaaaa")
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong passwrod."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': "Dear {} your password is updated successfully".format(self.object.username), 
                }
                return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''This view updating user password but only admin user can update password of company(user).
As only admins can access this view so no need of old password. Only new password and company
id required to change the password of that user'''
class AdminChangeCompanyPasswordView(generics.UpdateAPIView):
    serializer_class = AdminChangeCompanyPasswordSerializer
    model = User
    permission_classes = (permissions.IsAdminUser,)

    # method updating password for authenticated user after serializing.
    def update(self, request, *args, **kwargs):
        admin = self.request.user
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = User.objects.get(pk=serializer.data.get("company_id"))
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'message': "Dear {}, you successfully changed password for company named as {}.".format(admin.username, user.username), 
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



'''This Forget password view taking an email then checking if exist then check if user email is
verified or not if verified already then generate a brand new unique token for user and send an
reset password link with that token to user and also save token in User profile model named as UserTableDB'''
class ForgetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            if request.data['email']:
                pass
        except:
            return Response(status=status.HTTP_205_RESET_CONTENT)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            reg_obj= UserTableDB.objects.get(user=user)
            if reg_obj.isactive:
                reset_password_token = generate_token()
                # This is Content we need to send upon user password reset request
                email = {
                    "title": "Thank your for using BoosterTech.",
                    "shortDescription": "You have requested password reset",
                    "subtitle": "BoosterTech Business handling solution in one go",
                    "message": '''With the given link you will be moved to booster tech portal and you will be popped to enter a new password''',
                    'link': settings.PASSWORD_RESET_PROTOCOL + '://'+ settings.PASSWORD_RESET_DOMAIN +'/api/core/password/reset/token='+ reset_password_token,
                    'name': user.username
                    }
                subject = 'Password Reset'
                to_email = user.email
                send_email( email, subject, to_email, 'register.html') # sending email
                reg_obj.activation_key = reset_password_token #saving token for furhter use 
                reg_obj.is_activation_key_used = False #making activation key not used
                reg_obj.save()
                return Response({'message':'Reset Password link send Successfully'},status.HTTP_200_OK)
            else:
                return Response({'message':'User Not verified'},status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({'message': 'Email Not Exist'}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


'''In this view from post request getting activation_key and new password after that
check the UserProfile model UserTableDB if that activation key exists or not. If key
is there then check key is not already used. So, if key is fresh then update the password
for the user related to that key and sends an Confirmation email to user and return a 
response with success and HTTP status 200 OK else an message with HTTP 201'''
class ResetPsswordConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        activation_key = request.data['token']
        password= request.data['password']
        if UserTableDB.objects.filter(activation_key=activation_key).exists(): #Checking if token is available in database
            customer = UserTableDB.objects.get(activation_key=activation_key) #getting user profile against provided token
            if not customer.is_activation_key_used: # checking if token is already used or not?
                user= User.objects.get(email=customer.user.email) # getting user against present profile
                user.set_password(password)
                user.save()
                customer.is_activation_key_used=True
                customer.save()

                email = {
                    "title": "Thank your for using BoosterTech.",
                    "shortDescription": "You have requested password reset",
                    "subtitle": "Your Password has been reset successfully.",
                    "message": '''With the given link you will be moved to booster tech portal and you will be popped to enter a new password''',
                    'name': user.username
                    }
                subject = 'Password Reset Confirm'
                to_email = user.email
                send_email( email, subject, to_email, 'register.html')
                return Response({'message': 'Dear '+ user.username +', your Password Reset Successfully'},status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':"Link has been Expired"}, status.HTTP_400_BAD_REQUEST)
        return Response(status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

'''Getting user profile. This view take id of given model and return data related to that user.'''
class FetchUserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = FetchUserProfileSerializer
    permission_class = (permissions.IsAuthenticated,)

'''This view is for updating user profile. In view first of all we are checking if user exists if
yes then we check if user is superuser? if yes its mean he have permissions to update his profile
as well as companies profiles. That is why now we check if he have id of any company if yes
then we get that company and update that company profile else superuser profile.
now if in start, request is not from superuser then current user will be updated.'''
class UserProfileUpdateView(APIView):
    permission_class = (permissions.IsAuthenticated,)
    def post(self, request):
        user = self.request.user
        message = "Dear {} your Profile has been updated successfully".format(user.username)
        if user.is_superuser:
            try:
                if request.data['company_id']:
                    user = User.objects.get(pk=int(request.data['company_id']))
                    message = "Dear admin, Profile of Company named as {} has been updated successfully".format(user.username)
            except:
                pass

        if request.data['first_name'] and request.data['last_name'] and request.data['email']:
            user.user_profile.first_name = request.data['first_name']
            user.user_profile.last_name = request.data['last_name']
            try:
                validate_email(request.data['email'])
                if user.email == request.data['email']:
                    user.save()
                    user.user_profile.save()
                    return Response({"success": message}, status.HTTP_200_OK)
                elif not User.objects.filter(email=request.data['email']).exists():
                    user.email = request.data['email']
                    user.user_profile.isactive = False
                    user.save()
                    user.user_profile.save()
                    #here need to send activation email to user so he can confirm his new mail
                    return Response({"success": message + "Also as you have updated email so kindly check mailbox and verify your email"}, status.HTTP_202_ACCEPTED)
                else:
                    return Response({"validation_error": "Email should be unique."}, status.HTTP_205_RESET_CONTENT)
            except ValidationError as e:
                return Response({"validation_error":e}, status.HTTP_205_RESET_CONTENT)
        return Response({"message":"data not found"}, status.HTTP_204_NO_CONTENT)
        


'''This view is just accessible by the Super admin user and here we are
returning the list of all users except the admin hisself.
Also we are attaching the pagination class to this view so admin user can imit result from client side.'''
class CompaniesListAPIView(generics.ListAPIView):
    queryset = User.objects.filter(is_superuser=False)
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CompaniesFetchSerializer
    pagination_class = CompaniesLimitOffsetPagination

'''In this View we are using magic view of Django rest frame work named as DestroyAPIView in this we we
just need to pass permissions first that only admin user can do activity in this view and a query set
related to Model we want to perform task. here we are querying User model and only admin can delete any
user object. In this query we are filtering only those persons who is not superuser to avoid accidental
deletion of super user. This view just need an id of user in the URL and user will be deleted automatically'''
class CompanyDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.filter(is_superuser=False)
    permission_class = (permissions.IsAdminUser,)