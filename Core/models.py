from email.policy import default
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=255,null=True,blank=True, default="")
    last_name = models.CharField(max_length=255,null=True,blank=True, default="")
    picture = models.ImageField(blank=False,null=False, upload_to="profileImages", default="profileImages/image.jpg" )
    isactive = models.BooleanField(default=False,null=True)
    is_activation_key_used = models.BooleanField(default=True)
    activation_key = models.CharField(max_length=255, blank=True, null=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id) +"-"+ str(self.user.email)


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_company', )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.id) + " "+ self.name


class CompanyAccessRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_access')
    company = models.ForeignKey(Company, on_delete=models.CASCADE,)

    def __str__(self):
        return str(self.id) + "-" + self.company.name + "-"+ str(self.company.id)



'''This function recieving a signal from database whenever a User instance is created and on
every instance it also make profile object against that instance'''
@receiver(post_save, sender=User)
def createUserProfile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)