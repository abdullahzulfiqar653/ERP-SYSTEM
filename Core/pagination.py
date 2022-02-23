from rest_framework.pagination import LimitOffsetPagination



'''here we are overriding the LimitOffsetpagination to set the some parameters
and parameters for requet are explaining thereselves already'''
class CompaniesLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'myoffset'
    max_limit = 10