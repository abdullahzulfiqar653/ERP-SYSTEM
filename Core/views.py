from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from .models import UserTableDB
from .serializers import RegisterSerializer, ChangePasswordSerializer,CustomJWTSerializer
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import serializers
from utils.email import send_email
import random, string


'''Here we are customizing ObtainJSONWebToken View to return one more attribute is_admin so in client side 
developer can check the user logged in is an admin user or a simple user.'''
class CustomJWTView(ObtainJSONWebToken):
    serializer_class=CustomJWTSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response({
                'token': serializer.validated_data['token'],
                'is_admin': serializer.validated_data['is_admin']
            })
        else:
            raise serializers.ValidationError({"non_field_errors":"Account with this email/username does not exists"})


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

            # This is Content we need to send for email after registration process
            email = {
                "title": "Thank your for registering with BoosterTech Portal",
                "shortDescription": "These are the next steps.",
                "subtitle": "BoosterTech Business handling solution in one go",
                "message": '''You have successfully registered with BoosterTech. You can 
                        now login in to your profile and start. We have 
                        thousands of features just waiting for you to use. If you experience any 
                        issues feel free to contact our support at support@boostertech.com>'''
                    }
            subject = 'Welcome to Booster Tech'
            to_email = serializer.validated_data['email']
            send_email( email, subject, to_email, 'register.html')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": "Wrong passwrod."}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': "Dear {} your password is updated successfully".format(self.object.username), 
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''This Forget password view taking an email then checking if exist then check if user email is
verified or not if verified already then generate a brand new unique token for user and send an
reset password link with that token to user and also save token in User profile model named as UserTableDB'''
class ForgetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            reg_obj = UserTableDB.objects.get(user=user)
            
            if (reg_obj.isactive == True):
                reset_email_token = ''.join(
                    random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _
                    in range(200))
                while (UserTableDB.objects.filter(activation_key=reset_email_token).exists()):
                    reset_email_token = ''.join(
                        random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase)
                        for _
                        in
                        range(100))
                
                # This is Content we need to send upon user password reset request
                email = {
                    "title": "Thank your for using BoosterTech.",
                    "shortDescription": "You have requested password reset",
                    "subtitle": "BoosterTech Business handling solution in one go",
                    "message": '''With the given link you will be moved to booster tech portal and you will be popped to enter a new password''',
                    'link': 'http://localhost:3000/password/reset/activation_key='+ reset_email_token,
                    'name': user.username
                    }
                subject = 'Password Reset'
                to_email = user.email
                send_email( email, subject, to_email, 'register.html')
                reg_obj.activation_key = reset_email_token
                reg_obj.is_activation_key_used = False
                reg_obj.save()
                return Response({'message':'Reset Password link send Successfully'},status.HTTP_200_OK)
            else:
                return Response({'message':'User Not verify'},status.HTTP_200_OK)
        else:
            return Response({'message': 'Email Not Exist'}, status.HTTP_200_OK)


'''In this view from post request getting activation_key and new password after that
check the UserProfile model UserTableDB if that activation key exists or not. If key
is there then check key is not already used. So, if key is fresh then update the password
for the user related to that key and sends an Confirmation email to user and return a 
response with success and HTTP status 200 OK else an message with HTTP 201'''
class ResetPsswordConfirmView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        activation_key = request.data['activation_key']
        password= request.data['password']
        if(UserTableDB.objects.filter(activation_key=activation_key).exists()):
            customer = UserTableDB.objects.get(activation_key=activation_key)
            if customer.is_activation_key_used==False:
                user= User.objects.get(email=customer.user.email)
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
                return Response({'success':'Password Reset Successfully'},status.HTTP_202_ACCEPTED)
            else:
                return Response({'message':"Link has been Expired"},status.HTTP_201_CREATED)
        return Response(False)