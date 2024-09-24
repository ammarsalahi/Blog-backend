from rest_framework.pagination import PageNumberPagination

class NewsPagination(PageNumberPagination):
    page_size=8
    max_page_size=32
    page_size_query_param = 'page_size'