from django.core.management.base import BaseCommand
from users.models import Payment
from django.contrib.auth.models import User
from courses.models import Course, Lesson
from decimal import Decimal


class Command(BaseCommand):
    help = 'Создание платежей для пользователей'

    def handle(self, *args, **kwargs):
        # Пример создания платежа
        user = User.objects.first()  # Первый пользователь
        course = Course.objects.first()  # Первый курс
        lesson = Lesson.objects.first()  # Первый урок

        # Создание платежа
        payment = Payment.objects.create(
            user=user,
            course=course,
            lesson=None,  # Можно установить в None, если платеж за курс
            amount=Decimal('1000.00'),
            payment_method='cash',
            payment_date='2025-03-19T12:00:00Z'
        )

        self.stdout.write(self.style.SUCCESS(f'Платеж {payment.id} успешно создан!'))
