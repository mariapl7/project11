from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    page_size = 10  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр для запроса с указанием размера страницы
    max_page_size = 100  # Максимальный размер страницы, который можно запросить


class LessonPagination(PageNumberPagination):
    page_size = 5  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр для запроса с указанием размера страницы
    max_page_size = 50  # Максимальный размер страницы, который можно запросить
