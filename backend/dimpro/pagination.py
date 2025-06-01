from rest_framework.pagination import PageNumberPagination

class StardardResultsSetPagination(PageNumberPagination):
    page_size = 1000000 #idk, just change it if you see fit
    page_size_query_param = 'page_size'
    max_page_size = 10000

class LogsResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000000