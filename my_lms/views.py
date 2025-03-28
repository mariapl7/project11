from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from courses.models import Course


class CourseUpdateView(APIView):
    def put(self, request, send_course_update_email=None, *args, **kwargs):
        # Получаем курс по ID
        course_id = kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Обновляем информацию о курсе, например, название или описание
        course.name = request.data.get('name', course.name)
        course.description = request.data.get('description', course.description)
        course.save()

        # После обновления курса отправляем письма всем подписчикам
        send_course_update_email.delay(course.id)

        return Response({'status': 'Курс обновлен и уведомления отправлены!'})
