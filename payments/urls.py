from django.urls import path
from .views import PaymentListView
from .views import create_payment_view, payment_success, payment_cancel

urlpatterns = [
    path("create_payment/<int:product_id>/", create_payment_view, name="create_payment"),
    path("payment/success/", payment_success, name="payment_success"),
    path("payment/cancel/", payment_cancel, name="payment_cancel"),
    path('payments/', PaymentListView.as_view(), name='payment-list'),
]
