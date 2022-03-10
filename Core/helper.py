import random, string
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
