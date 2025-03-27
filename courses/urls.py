from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet
from .views import CourseListView, LessonListView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Это подключает ваши ViewSet к URL
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
]
