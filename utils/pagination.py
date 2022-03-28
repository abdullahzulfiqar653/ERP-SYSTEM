from rest_framework.pagination import LimitOffsetPagination


'''here we are overriding the LimitOffsetpagination to set some parameters
and overrided parameters explaining thereselves already. This override is
for the admin user accessing all users(companies) So, not to return all
users in one go when we will have hundered or thousands of users'''


class LimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'myoffset'
    max_limit = 15
