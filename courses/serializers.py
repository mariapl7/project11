from rest_framework import serializers
from .models import Course, Lesson, Subscription
from my_lms.validators import youtube_link_validator


# Сериализатор для модели Course
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

    # Описание полей
    title = serializers.CharField(help_text="Название курса")
    description = serializers.CharField(help_text="Описание курса")


# Сериализатор для модели Lesson
class LessonSerializer(serializers.ModelSerializer):
    # Добавление валидатора к полю video_url
    video_url = serializers.URLField(validators=[youtube_link_validator])

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'video_url', 'course', 'owner']

    # Описание полей
    title = serializers.CharField(help_text="Название урока")
    content = serializers.CharField(help_text="Содержание урока")
    video_url = serializers.URLField(help_text="Ссылка на видеоурок")
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), help_text="Курс, к которому относится урок")
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), help_text="Владелец урока")
