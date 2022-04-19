from django.contrib.auth.models import User
from Core.models import Company
from Lookup.models import LookupType, LookupName, AccountType
from Contact.models import Contact
from rest_framework import status
import pytest
from model_bakery import baker


@pytest.fixture
def create_user_company_and_contact(api_client):
    def do_create_user_and_company(isactive=True, is_staff=True):
        user = baker.make(User, email='someone@example.com', is_staff=is_staff)
        user.set_password('haha@123')
        user.save()
        user.user_profile.isactive = isactive
        user.user_profile.save()
        user_response = api_client.post('/api/core/login/', {
            "email": 'someone@example.com',
            "password": 'haha@123'
        })
        company = baker.make(Company, user=user)
        lookup_type = baker.make(LookupType)
        lookup_name = baker.make(LookupName, lookup_type=lookup_type)
        # tax = baker.make(Tax, lookup_name=lookup_name)
        account_type = baker.make(AccountType, category=lookup_name)
        # payment_day = baker.make(PaymentDay, lookup_name=lookup_name)
        contact = baker.make(Contact, company=company, contact_type=lookup_name, account_type=account_type, )
        headers = {
            'HTTP_AUTHORIZATION': "JWT {}".format(user_response.data['token']),
            'HTTP_COMPANY': company.id
            }
        return {
            'contact': contact,
            'headers': headers
        }

    return do_create_user_and_company


@pytest.fixture
def create_invoice(api_client):
    def do_create_invoice(data, headers):

        response = api_client.post('/api/sales/invoice/', data, **headers)
        return response
    return do_create_invoice

# ---------------------------------------------------------------------------------------------- #
# ------------------------------------Invoice Model Test Cases------------------------------------- #
# ---------------------------------------------------------------------------------------------- #


@pytest.mark.django_db
class TestInvoice:
    def test_if_invoice_payload_is_invalid_return_400(self, create_user_company_and_contact, create_invoice):
        response = create_user_company_and_contact()

        invoice_response = create_invoice({
            "invoice_items": [
                {
                    "quantity": 1,
                    "description": "aaaaaaaaaaaaaaaaaaa",
                    "price": 22.22,
                    "discount": 22.00,
                    "base": 12.12,
                    "invoice": 1
                }
                ],
            "invoice_date": "2022-12-12",
            # "client": response['contact'].id,
            # "account": response['contact'].account_type.id,

            "base_amount": 2000,
            "vat_percentage": 2.2,
            "vat_total": 500,
            "ret_percentage": 1,
            "ret_total": 500,
            "total": 3000,
            # "payment_method": response['contact'].contact_type.id,
            "due_date": "2022-12-12",
            "iban": "hxiqix",
            "tax_address": "scd",
            "tax_postcode": "asx",
            "tax_province": "ax",
            "shipping_address": "XZ",
            "shipping_postcode": "WERWDEW",
            "shipping_province": "EWEW",
            # "tax_country": 1,
            # "shipping_country": 1
        }, response["headers"])
        assert invoice_response.status_code == status.HTTP_400_BAD_REQUEST
