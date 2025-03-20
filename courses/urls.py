from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet
# courses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(router.urls)),  # Это подключает ваши ViewSet к URL
]
