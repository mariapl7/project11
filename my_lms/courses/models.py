from django.db import models
from users.models import CustomUser
from rest_framework import serializers
from .models import Course
from django.contrib.auth.models import User
from .lesson import Lesson
from django.core.management.base import BaseCommand
from users.models import Payment, Course, Lesson
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Payment, Lesson, Course
from .lesson import LessonSerializer
import django_filters
from .models import Payment


class Course(models.Model):
    title = models.CharField(max_length=200)
    preview_image = models.ImageField(upload_to='course_previews/')
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='lesson_previews/')
    video_link = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return self.title


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'description', 'lesson_count']

    def get_lesson_count(self, obj):
        # Возвращаем количество уроков в курсе
        return obj.lessons.count()


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('bank_transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)  # Оплаченный курс
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)  # Оплаченный урок
    payment_date = models.DateTimeField(auto_now_add=True)  # Дата оплаты
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма оплаты
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)  # Способ оплаты

    def __str__(self):
        return f"Payment by {self.user.username} on {self.payment_date} for {self.amount} ({self.payment_method})"


class Command(BaseCommand):
    help = 'Создает записи о платежах для теста'

    def handle(self, *args, **kwargs):
        user1 = User.objects.get(id=1)
        course1 = Course.objects.get(id=1)
        lesson1 = Lesson.objects.get(id=1)

        Payment.objects.create(
            user=user1,
            course=course1,
            lesson=None,
            payment_date="2025-03-12T12:00:00Z",
            amount=1000.00,
            payment_method="cash"
        )

        Payment.objects.create(
            user=user1,
            course=None,
            lesson=lesson1,
            payment_date="2025-03-13T15:30:00Z",
            amount=500.00,
            payment_method="bank_transfer"
        )

        self.stdout.write(self.style.SUCCESS('Successfully created payment records'))


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)  # Включаем все уроки, связанные с курсом

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        # Возвращаем количество уроков в курсе
        return obj.lessons.count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'course', 'lesson', 'payment_date', 'amount', 'payment_method']


class PaymentFilter(django_filters.FilterSet):
    # Фильтр по дате оплаты
    payment_date = django_filters.DateFromToRangeFilter(field_name='payment_date')

    # Фильтр по курсу
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all(), field_name='course')

    # Фильтр по уроку
    lesson = django_filters.ModelChoiceFilter(queryset=Lesson.objects.all(), field_name='lesson')

    # Фильтр по способу оплаты
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ['payment_date', 'course', 'lesson', 'payment_method']
