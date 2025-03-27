from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Payment
from .serializers import PaymentSerializer
from .filters import PaymentFilter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import create_payment_link


class PaymentListView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PaymentFilter  # Устанавливаем наш фильтр
    ordering_fields = ['payment_date']  # Устанавливаем возможность сортировки по дате
    ordering = ['payment_date']  # Сортировка по умолчанию по дате


@csrf_exempt
def create_payment_view(request, product_id):
    if request.method == "POST":
        try:
            payment_link = create_payment_link(product_id)
            return JsonResponse({"payment_link": payment_link}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Only POST requests are allowed."}, status=405)

def payment_success(request):
    return JsonResponse({"message": "Payment was successful!"})

def payment_cancel(request):
    return JsonResponse({"message": "Payment was canceled!"})
