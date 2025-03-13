from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Payment
from ..courses.models import PaymentSerializer


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Можно добавить другие обязательные поля


class UserPaymentHistorySerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True)  # Включаем все платежи для пользователя

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'payments']

    def get_payments(self, obj):
        # Возвращаем только платежи, которые связаны с этим пользователем
        return PaymentSerializer(Payment.objects.filter(user=obj), many=True).data
