from rest_framework import serializers
from .models import Course, Lesson



class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'lesson_count', 'number_of_lessons', 'lessons']

    def get_lesson_count(self, obj):
        # Возвращаем количество уроков для данного курса
        return obj.lessons.count()  # Используем related_name 'lessons', чтобы получить все уроки

    def get_number_of_lessons(self, obj):
        # Получаем количество уроков для этого курса
        return obj.lessons.count()


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'created_at']  # Укажите необходимые поля модели Lesson
