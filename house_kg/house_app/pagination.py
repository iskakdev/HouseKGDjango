from rest_framework.pagination import PageNumberPagination
from .models import Property


class PropertyPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 25
