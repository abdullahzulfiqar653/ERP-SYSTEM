from django.shortcuts import get_object_or_404
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from Core.models import Company, CompanyAccessRecord
from re import sub


def get_company_if_authenticated(user, company_id):
    if (user.is_staff and Company.objects.filter(
            pk=company_id, user=user).exists()) or \
        CompanyAccessRecord.objects.filter(
            user=user, company_id=company_id):
        return get_object_or_404(Company, pk=company_id)
    else:
        return Company.DoesNotExist


class CompanyAccessMiddleWare:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # This code is executed just before the view is called
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        company_id = request.META.get('HTTP_COMPANY')
        request.company = None
        if header_token is not None:
            try:
                token = sub('JWT ', '', request.META.get('HTTP_AUTHORIZATION', None))
                verified_data = VerifyJSONWebTokenSerializer().validate({'token': token})
                if Company.objects.filter(pk=company_id).exists():
                    company = get_company_if_authenticated(verified_data['user'], company_id)
                    if not isinstance(company, Company):
                        return None
                    else:
                        request.company = company
                        return None
                else:
                    return None
            except Exception as e:
                return None
                print(e)
        return None

    # This code is executed if an exception is raised
    # def process_exception(request, exception):
    #     return exception

    # def process_template_response(request, response):
    #     print("process_template_response")
    #     # This code is executed if the response contains a render() method
    #     return response
