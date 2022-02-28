from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UserTableDB(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=255,null=True,blank=True)
    last_name = models.CharField(max_length=255,null=True,blank=True)
    picture = models.TextField(blank=True,null=True,)
    isactive = models.BooleanField(default=False,null=True)
    is_activation_key_used = models.BooleanField(default=True)
    activation_key = models.CharField(max_length=255, blank=True, null=True)

'''This function recieving a signal from database whenever a User instance is created and on
every instance it also make profile object against that instance'''
@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        UserTableDB.objects.create(user=instance)