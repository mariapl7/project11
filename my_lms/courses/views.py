from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from .models import Course, Lesson, PaymentFilter
from .serializers import CourseSerializer, FullLessonSerializer, ShortLessonSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from django_filters.rest_framework import DjangoFilterBackend


class CourseListView(APIView):
    def get(self, request):
        # Здесь вы можете вернуть список курсов
        courses = [
            {"id": 1, "title": "Курс 1", "description": "Описание курса 1"},
            {"id": 2, "title": "Курс 2", "description": "Описание курса 2"},
        ]
        return Response(courses, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer  # Используй сериализатор, который тебе нужен


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = ShortLessonSerializer  # Используем сокращенный сериализатор для списка


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = FullLessonSerializer  # Используем полный сериализатор для детального просмотра/обновления


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # По умолчанию сортируем по убыванию даты
