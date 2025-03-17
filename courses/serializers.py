from rest_framework import serializers
from .models import Course, Lesson, Payment


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class FullLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ShortLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content']


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = ShortLessonSerializer(many=True)  # Включаем только необходимые уроки

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
