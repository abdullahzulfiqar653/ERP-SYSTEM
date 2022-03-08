from urllib import response
from urllib.request import Request
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
from django.db.models import Q

from utils.pagination import LimitOffsetPagination
from utils.email import send_email
from .models import UserProfile, Company, CompanyAccessRecord
from.helper import generate_token
from .serializers import (
        RegisterSerializer,
        ChangePasswordSerializer,
        CustomJWTSerializer,
        CompaniesFetchSerializer,
        FetchUserProfileSerializer,
        AdminChangeUserPasswordSerializer,
        CompanyCreateSerializer,
        CompanyAccessSerializer,
    )


'''
Here we are customizing ObtainJSONWebToken View to return two more attribute is_admin and email so in client side 
developer can check the user logged in is an admin user or a simple user and email for display.
'''
class CustomJWTView(ObtainJSONWebToken):
    serializer_class=CustomJWTSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            if not user.user_profile.isactive:
                return Response({'message':'Oops, Your email is not verified. Kindly verify your email to continue.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({
                'token': serializer.validated_data['token'],
                'is_admin': serializer.validated_data['is_admin'],
                'email': serializer.validated_data['email']
            }, status.HTTP_200_OK)
        else:
            raise serializers.ValidationError({"message":"Account with provided credentials does not exists."}, status.HTTP_400_BAD_REQUEST)


'''
This View is for registration of admin. An admin can register his self base on 4 arguments:
 email, username and a strong password and retyped password. This View check the validations
and if all 4 arguments are Correct then admin will be registered and recieve an email of Welcome
and also a link attached so that he can verify his email through that link.
'''
class AdminRegisterAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    def post(self, request, format='json'):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.validated_data['email'])
            user.is_staff = True
            
            email_activation_token = generate_token()
            # This is Content we need to send for email after registration process
            email = {
                "title": "Thank your for registering with BoosterTech Portal",
                "shortDescription": "These are the next steps.",
                "subtitle": "BoosterTech Business handling solution in one go",
                'link': settings.PASSWORD_RESET_PROTOCOL + '://'+ settings.PASSWORD_RESET_DOMAIN +'/activate/activation_key='+ email_activation_token,
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
            user.save()
            user.user_profile.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
This View is for registration of users. Only admin can register user for his company based on 4 arguments:
 email, username and a strong password and retyped password. This View check the validations
and if all 4 arguments are Correct then user will be registered and recieve an email of Welcome
and also a link attached so that he can verify his email through that link.
'''
class UserRegisterAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = RegisterSerializer
    def post(self, request, format='json'):
        serializer = self.serializer_class(data=request.data)
        adminUser = self.request.user
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.validated_data['email'])
            user.user_profile.admin = adminUser
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
            user.save()
            user.user_profile.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
This view accepting post request and in the payload clientside will send an activation_key
after that this view checks if the key exists or not if exist then verify if it is already used
or a fresh key, if it is a fresh key then find the user against that key and  make that user active.
'''
class UserEmailVerifyView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            if request.data['activation_key']:
                pass
        except:
            return Response(status=status.HTTP_205_RESET_CONTENT)
        activation_key = request.data['activation_key']
        if UserProfile.objects.filter(activation_key=activation_key).exists():
            customer = UserProfile.objects.get(activation_key=activation_key)
            if not customer.is_activation_key_used:
                customer.isactive = True
                customer.is_activation_key_used = True
                customer.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


'''
This view is for users who want to update their password. This View updating password for
admin or simple users except those who are not authenticated. This View first checking if
old password is rite then serialzer validating the password and password1 if they
are matched then updating password.
'''
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
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


'''
This view updating user password but only admin user can update password of company(user).
As only admins can access this view so no need of old password. Only new password and company
id required to change the password of that user
'''
class AdminChangeUserPasswordView(generics.UpdateAPIView):
    serializer_class = AdminChangeUserPasswordSerializer
    permission_classes = (permissions.IsAdminUser,)

    # method updating password for authenticated user after serializing.
    def update(self, request, *args, **kwargs):
        admin = self.request.user
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            user = User.objects.get(pk=serializer.data.get("user_id"))
            if not user.user_profile.admin == self.request.user:
                return Response({"message": "you are an unauthorized user to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                'message': "Dear {}, you successfully changed password for user named as {}.".format(admin.username, user.username), 
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
This Forget password view taking an email then checking if it exist then check if user email is
verified or not if verified already then generate a brand new unique token for user and send an
reset password link with that token to user and also save token in User profile model named as UserProfile
'''
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
            reg_obj= UserProfile.objects.get(user=user)
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


'''
In this view from post request getting activation_key and new password after that
check the UserProfile model UserProfile if that activation key exists or not. If key
is there then check key is not already used. So, if key is fresh then update the password
for the user related to that key and sends an Confirmation email to user and return a 
response with success and HTTP status 200 OK else an message with HTTP 201
'''
class ResetPsswordConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        activation_key = request.data['token']
        password= request.data['password']
        if UserProfile.objects.filter(activation_key=activation_key).exists(): #Checking if token is available in database
            customer = UserProfile.objects.get(activation_key=activation_key) #getting user profile against provided token
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


'''
Getting user profile. This view take id in URL and return profile related to that user.
'''
class FetchUserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = FetchUserProfileSerializer
    permission_class = (permissions.IsAuthenticated,)


'''
This view is for updating user profile. In view first of all we are checking if user exists if
yes then we check if user is superuser? if yes its mean he have permissions to update his profile
as well as companies profiles. That is why now we check if he have id of any company if yes
then we get that company and update that company profile else superuser profile.
now if in start, request is not from superuser then current user will be updated.
'''
class UserProfileUpdateView(APIView):
    permission_class = (permissions.IsAuthenticated,)
    def put(self, request):
        user = self.request.user
        message = "Dear {} your Profile has been updated successfully".format(user.username)
        if user.is_staff:
            try:
                if request.data['user_id']:
                    user = User.objects.get(pk=int(request.data['user_id']))
                    message = "Dear admin, Profile of User named as {} has been updated successfully".format(user.username)
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
                    return Response({"success": message + " Also as you have updated email so kindly check mailbox and verify your email"}, status.HTTP_202_ACCEPTED)
                else:
                    return Response({"validation_error": "Email should be unique."}, status.HTTP_205_RESET_CONTENT)
            except ValidationError as e:
                return Response({"validation_error":e}, status.HTTP_205_RESET_CONTENT)
        return Response({"message":"data not found"}, status.HTTP_204_NO_CONTENT)


'''
This View in post request recieving user_id and a list of companies after that view check if user is the subuser
of current user if yes then verify the company if company is of the current user then check if it is alreaedy
assigned to the same user or someone else under the same admin If not then create a new permission for the user
to access all those companies and remove any removed requested company
'''
class CompanyAccessView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CompanyAccessSerializer
    def post(self, request, *args, **kwargs):
        adminUser = self.request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if User.objects.filter(pk=int(request.data['user_id'])).exists():
                user = User.objects.filter(pk=int(request.data['user_id'])).first()
                if user.user_profile.admin == adminUser:
                    
                    already_assigned_list = list(CompanyAccessRecord.objects.filter(user=user).values_list('company_id', flat=True))
                    permission_remove_list = list(set(already_assigned_list) - set(request.data['company_list']))
                    for company_id in request.data['company_list']:
                        if Company.objects.filter(pk=company_id, user=adminUser).exists(): 
                            if company_id in CompanyAccessRecord.objects.all().values_list('company',flat=True): #ok
                                if CompanyAccessRecord.objects.get(company=company_id).id in list(CompanyAccessRecord.objects.filter(user=user).values_list('id', flat=True)):
                                    continue
                                else:
                                    return response({"message": "company already assigned to other user"})
                            else:
                                record = CompanyAccessRecord(user=user, company=Company.objects.get(pk=company_id))
                                record.save()
                    for company_id in permission_remove_list:
                        obj = CompanyAccessRecord.objects.get(company_id=company_id)
                        obj.delete()
                    return Response({"message":"Permissions created."},status=status.HTTP_201_CREATED)
                        
                return Response({"message":"you dont have permission for this user"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({"message":"user not exists"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_205_RESET_CONTENT)



'''
This View getting post request with data and validating name field for company after
that creating company with that name or raise errors if any
'''
class AddCompanyAPIView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = CompanyCreateSerializer
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            Company.objects.create(user=self.request.user, name=request.data['name'])
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



'''
This view is just accessible by the Super admin user and here we are returning the list of all users
except the admin hisself. Also we are attaching the pagination class to this view so admin user can
imit result from client side.
'''
class CompaniesListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompaniesFetchSerializer
    pagination_class = LimitOffsetPagination
    def get_queryset(self):
        user = self.request.user
        if not self.request.user.is_staff:
            return Company.objects.filter(user=user)
        else:
            return Company.objects.filter(user=user)


class UserCompaniesListAPIView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CompaniesFetchSerializer
    pagination_class = LimitOffsetPagination
    def get_queryset(self):
        user = self.request.user
        adminuser = User.objects.get(pk=user.affiliate)
        companies = Company.objects.filter(user=adminuser).values_list('id', flat=True)

        ids = ImaginaryTable.objects.filter( Q(user=user.id) and Q(affiliate_id=user.affilate)).values_list('company_id', flat=True)
        return Company.objects.filter(user=user)



'''
In this View we are using magic view of Django rest frame work named as DestroyAPIView in this we we
just need to pass permissions first that only admin user can do activity in this view and a query set
related to Model we want to perform task. here we are querying User model and only admin can delete any
user object. In this query we are filtering only those persons who is not admin to avoid accidental
deletion of super user. This view just need an id of user in the URL and user will be deleted automatically
'''
class UserDeleteAPIView(generics.DestroyAPIView):
    queryset = User.objects.filter(is_staff=False)
    permission_class = (permissions.IsAdminUser,)

    def perform_destroy(self, instance):
        if not UserProfile.objects.filter(user=instance.id, admin=self.request.user.id).exists():
            return Response({"message": "you are an unauthorized user to perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            super().perform_destroy(instance)
