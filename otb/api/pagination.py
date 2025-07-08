from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """Пагинация для пассажиров."""

    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 30
