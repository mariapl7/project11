from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Course, Lesson
from rest_framework.reverse import reverse
from django.conf import settings


class LessonTests(APITestCase):
    def setUp(self):
        # Создание тестовых пользователей
        self.user = User.objects.create_user(username='user1', password='password')
        self.admin_user = User.objects.create_superuser(username='admin', password='password')

        # Создание курса
        self.course = Course.objects.create(title="Test Course", description="Course description",
                                            owner=self.admin_user)

        # Создание уроков для тестирования
        self.lesson = Lesson.objects.create(title="Test Lesson", content="Lesson content", course=self.course,
                                            owner=self.admin_user)

    def test_create_lesson(self):
        url = reverse('lesson-list')
        data = {
            'title': 'New Lesson',
            'content': 'New content for lesson',
            'course': self.course.id,
        }

        # Проверка создания урока для авторизованного пользователя
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)  # Один урок уже существует, плюс новый

    def test_get_lessons(self):
        url = reverse('lesson-list')
        # Проверка получения уроков без аутентификации
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Должен быть один урок

    def test_update_lesson(self):
        url = reverse('lesson-detail', args=[self.lesson.id])
        data = {'title': 'Updated Lesson', 'content': 'Updated content', 'course': self.course.id}

        # Проверка обновления урока администратором
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, 'Updated Lesson')

    def test_delete_lesson(self):
        url = reverse('lesson-detail', args=[self.lesson.id])

        # Проверка удаления урока администратором
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)  # Урок должен быть удален

    def test_create_lesson_as_user(self):
        url = reverse('lesson-list')
        data = {
            'title': 'New Lesson',
            'content': 'Lesson content',
            'course': self.course.id,
        }

        # Проверка, что обычный пользователь не может создавать уроки
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Ожидаем ошибку доступа


class SubscriptionTests(APITestCase):
    def setUp(self):
        # Создание тестовых пользователей
        self.user = User.objects.create_user(username='user1', password='password')
        self.another_user = User.objects.create_user(username='user2', password='password')
        self.admin_user = User.objects.create_superuser(username='admin', password='password')

        # Создание курса
        self.course = Course.objects.create(title="Test Course", description="Course description",
                                            owner=self.admin_user)

    def test_subscribe_to_course(self):
        url = reverse('subscribe')

        # Подписка пользователя на курс
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Подписка добавлена', response.data['message'])

    def test_unsubscribe_from_course(self):
        # Подписка пользователя на курс
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        self.client.post(reverse('subscribe'), data, format='json')

        # Отписка от курса
        response = self.client.post(reverse('subscribe'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Подписка удалена', response.data['message'])

    def test_subscribe_as_another_user(self):
        url = reverse('subscribe')

        # Попытка подписать другого пользователя
        self.client.force_authenticate(user=self.another_user)
        data = {'course_id': self.course.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Подписка добавлена', response.data['message'])

    def test_subscription_exists(self):
        url = reverse('subscribe')

        # Подписка пользователя
        self.client.force_authenticate(user=self.user)
        data = {'course_id': self.course.id}
        self.client.post(url, data, format='json')

        # Проверка подписки
        response = self.client.get(reverse('course-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(course['is_subscribed'] for course in response.data))

    def test_unauthorized_user_subscription(self):
        url = reverse('subscribe')
        data = {'course_id': self.course.id}

        # Попытка подписки без аутентификации
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Пользователь не авторизован
