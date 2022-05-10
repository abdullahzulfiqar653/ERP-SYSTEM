from .models import Contact


def get_contact_id(contact_type):
    contact_type_name = contact_type.lookup_name.lower()
    if contact_type_name == "client":
        start = 430000000001
        # end = 439999999999
        if not Contact.objects.filter(contact_type=contact_type).exists():
            return start
        contact_id = Contact.objects.filter(
            contact_type=contact_type).latest('id').contact_id
        return str(int(contact_id) + 1)

    elif contact_type_name == "debitor":
        start = 440000000001
        # end = 449999999999
        if not Contact.objects.filter(contact_type=contact_type).exists():
            return start
        contact_id = Contact.objects.filter(
            contact_type=contact_type).latest('id').contact_id
        return str(int(contact_id) + 1)

    elif contact_type_name == "provider":
        start = 400000000001
        # end = 409999999999
        if not Contact.objects.filter(contact_type=contact_type).exists():
            return start
        contact_id = Contact.objects.filter(
            contact_type=contact_type).latest('id').contact_id
        return str(int(contact_id) + 1)

    elif contact_type_name == "creditor":
        start = 410000000001
        # end = 419999999999
        if not Contact.objects.filter(contact_type=contact_type).exists():
            return start
        contact_id = Contact.objects.filter(
            contact_type=contact_type).latest('id').contact_id
        return str(int(contact_id) + 1)
    else:
        return 000000000000
