from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer,  LessonSerializer, RegisterSerializer
from rest_framework import viewsets
from .models import Course, Lesson, Subscription
from .permissions import IsOwner
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # Для того чтобы пользователи могли регистрироваться без авторизации
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": serializer.data,
                "message": "User registered successfully!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        return self.register(request)  # Для регистрации


class UserPaymentHistorySerializer:
    pass


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # Получаем текущего аутентифицированного пользователя
        serializer = UserPaymentHistorySerializer(user)
        return Response(serializer.data)


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class IsModerator(permissions.BasePermission):
    """
    Разрешает доступ только пользователям, которые являются модераторами.
    """
    def has_permission(self, request, view):
        # Проверяем, состоит ли пользователь в группе "moderators"
        return request.user.groups.filter(name='moderators').exists()


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Получаем пользователя из запроса
        user = request.user

        # Получаем id курса из данных запроса
        course_id = request.data.get('course_id')

        # Получаем курс из базы данных
        course = get_object_or_404(Course, id=course_id)

        # Проверяем, существует ли уже подписка на этот курс для данного пользователя
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)

        if not created:
            # Если подписка уже существует, то удаляем ее
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)


class CourseViewSet:
    pass


class LessonViewSet:
    pass


def custom_404(request, exception):
    return HttpResponseNotFound("Страница не найдена")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_description="Получение списка всех пользователей")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Создание нового пользователя")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
