from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class HolidayPagination(LimitOffsetPagination):
    default_limit = 3
    max_limit = 4
    limit_query_param = 'limit'
    offset_query_param = 'start'
