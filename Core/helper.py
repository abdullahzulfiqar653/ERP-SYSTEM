import string
import random
from django.contrib.auth.models import User
from .models import UserProfile


def generate_token():
    token = ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase +
            string.digits +
            string.ascii_lowercase
        ) for _ in range(200))
    while (UserProfile.objects.filter(activation_key=token).exists()):
        token = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase +
                string.digits +
                string.ascii_lowercase
            )for _ in range(150))
    return token


def generate_username():
    username = ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase +
            string.digits +
            string.ascii_lowercase
        ) for _ in range(20))
    while (User.objects.filter(username=username).exists()):
        username = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase +
                string.digits +
                string.ascii_lowercase
            )for _ in range(20))
    return username
