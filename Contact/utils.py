from .models import Contact
import random


def get_contact_id(contact_type):
    contact_type_name = contact_type.lookup_name.lower()
    if contact_type_name == "client":
        random_num = random.randint(430000000001, 439999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(430000000001, 439999999999)
        return random_num

    elif contact_type_name == "debitor":
        random_num = random.randint(440000000001, 449999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(440000000001, 449999999999)
        return random_num

    elif contact_type_name == "provider":
        random_num = random.randint(400000000001, 409999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(400000000001, 409999999999)
        return random_num

    elif contact_type_name == "creditor":
        random_num = random.randint(410000000001, 419999999999)
        while Contact.objects.filter(contact_id=random_num).exists():
            random_num = random.randint(410000000001, 419999999999)
        return random_num
    else:
        return False
