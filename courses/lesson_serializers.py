from rest_framework import serializers
from .models import Lesson  # Импорт модели Lesson, если она есть


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content']
