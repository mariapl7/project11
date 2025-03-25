from rest_framework import serializers
from .models import Course, Lesson
from my_lms.validators import youtube_link_validator
from .models import Subscription


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'owner']


class LessonSerializer(serializers.ModelSerializer):
    # Добавление валидатора к полю video_url
    video_url = serializers.URLField(validators=[youtube_link_validator])

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'course', 'owner']


# serializers.py
from rest_framework import serializers
from .models import Course, Subscription


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_subscribed']

    def get_is_subscribed(self, obj):
        # Получаем текущего пользователя
        user = self.context.get('request').user

        # Проверяем, есть ли подписка на данный курс
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
