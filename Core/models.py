from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.models import User

class UserTableDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    picture = models.TextField(blank=True,null=True,)
    isactive = models.BooleanField(default=False,null=True)
    is_activation_key_used = models.BooleanField(default=True)
    activation_key = models.CharField(max_length=255, blank=True, null=True)