from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseListView, LessonListCreateView, LessonRetrieveUpdateDestroyView


router = DefaultRouter()
router.register(r'courses', CourseViewSet)


urlpatterns = [
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('', include(router.urls)),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
]