from rest_framework .pagination import PageNumberPagination, LimitOffsetPagination


class PaginationCount(PageNumberPagination):
    page_size = 10

class LimitOffsetPaginationCount(LimitOffsetPagination):
    default_limit = 20