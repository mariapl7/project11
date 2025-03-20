from rest_framework import viewsets
from .models import Course,Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Разделение прав для разных действий в ViewSet.
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]  # Создавать курсы могут только авторизованные
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]  # Список доступен всем авторизованным пользователям
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsAuthenticated, IsModerator]  # Модераторы могут редактировать и просматривать
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]  # Удалять могут только администраторы
        return super().get_permissions()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsAuthenticated, IsModerator]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
