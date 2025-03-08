from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)  # только через роутер

urlpatterns = [
    path('', include(router.urls)),  # все эндпоинты для курса
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),  # эндпоинт для списка уроков
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),  # эндпоинт для конкретного урока
]
