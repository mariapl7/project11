from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView
from .views import PaymentViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Все эндпоинты для курсов и платежей
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),  # Эндпоинт для списка уроков
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),  # Эндпоинт для конкретного урока
]
