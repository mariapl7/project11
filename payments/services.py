import stripe
from django.conf import settings
from .models import Product, Payment

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_product_and_price(product_id):
    product = Product.objects.get(id=product_id)
    stripe_product = stripe.Product.create(
        name=product.title,
        description=product.description,
    )

    stripe_price = stripe.Price.create(
        product=stripe_product.id,
        unit_amount=int(product.price * 100),  # Цена в копейках
        currency="usd",
    )

    return stripe_product, stripe_price

def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price": price_id,
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:8000/payment/success/",
        cancel_url="http://localhost:8000/payment/cancel/",
    )
    return session


def create_payment_link(product_id):
    stripe_product, stripe_price = create_product_and_price(product_id)
    session = create_checkout_session(stripe_price.id)

    payment = Payment.objects.create(
        product=Product.objects.get(id=product_id),
        stripe_session_id=session.id,
        payment_link=session.url,
    )

    return payment.payment_link
