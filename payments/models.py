from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson  # Убедитесь, что модели курсов и уроков существуют

User = get_user_model()  # Получаем кастомную модель пользователя, если она есть


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=8, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} for {self.course or self.lesson} by {self.user}"
