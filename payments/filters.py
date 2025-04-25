import django_filters

from courses.models import Course, Lesson
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all(), label="Курс")  # Если у вас есть модель Course
    lesson = django_filters.ModelChoiceFilter(queryset=Lesson.objects.all(), label="Урок")  # Если у вас есть модель Lesson
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES, label="Способ оплаты")
    date = django_filters.DateFromToRangeFilter(field_name="payment_date", label="Дата оплаты")

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method', 'payment_date']
