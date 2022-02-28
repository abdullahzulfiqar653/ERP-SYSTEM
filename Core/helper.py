import random, string
from .models import UserTableDB


def generate_token():
    token = ''.join(
        random.SystemRandom().choice(
            string.ascii_uppercase +
            string.digits +
            string.ascii_lowercase
            ) for _ in range(200))
    while (UserTableDB.objects.filter(activation_key=token).exists()):
        token = ''.join(
            random.SystemRandom().choice(
                string.ascii_uppercase + 
                string.digits +
                string.ascii_lowercase
                )for _ in range(150))
    return token
