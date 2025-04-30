from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PaymentFilter  # Устанавливаем наш фильтр
    ordering_fields = ['payment_date']  # Устанавливаем возможность сортировки по дате
    ordering = ['payment_date']  # Сортировка по умолчанию по дате
