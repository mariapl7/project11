from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from courses.models import Course
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta


class UserSubscription:
    pass


@shared_task
def send_course_update_email(course_id):
    # Получаем курс по его ID
    course = Course.objects.get(id=course_id)

    # Получаем всех пользователей, которые подписаны на обновления этого курса
    subscribers = UserSubscription.objects.filter(course=course)

    # Отправляем письмо каждому подписчику
    for subscription in subscribers:
        user = subscription.user
        send_mail(
            subject=f"Обновление курса {course.name}",
            message=f"Курс '{course.name}' был обновлен. Проверьте его содержание!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )


@shared_task
def deactivate_inactive_users():
    # Получаем текущую дату и время
    now = timezone.now()

    # Определяем дату более месяца назад
    month_ago = now - timedelta(days=30)

    # Ищем пользователей, которые не входили в систему более месяца
    inactive_users = User.objects.filter(last_login__lte=month_ago, is_active=True)

    # Блокируем этих пользователей
    for user in inactive_users:
        user.is_active = False
        user.save()

    return f"Блокировка пользователей: {inactive_users.count()}"
