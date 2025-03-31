from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Получаем модель User
User = get_user_model()

# Сериализатор для пользователя
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Создание пользователя с хешированием пароля
        user = User.objects.create_user(**validated_data)
        return user


# Сериализатор для регистрации пользователя
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        # Проверка, что пароли совпадают
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        # Создание пользователя
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course  # Убедитесь, что модель Course существует
        fields = '__all__'  # Заполните, если нужно

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson  # Убедитесь, что модель Lesson существует
        fields = '__all__'  # Заполните, если нужно

