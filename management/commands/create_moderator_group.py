from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу модераторов и назначает соответствующие права на работу с уроками и курсами'

    def handle(self, *args, **kwargs):
        # Создаем группу модераторов, если она еще не существует
        group, created = Group.objects.get_or_create(name='Moderators')

        # Пример прав для модераторов (для уроков и курсов)
        permissions = Permission.objects.filter(codename__in=['change_lesson', 'change_course', 'delete_lesson', 'delete_course'])

        # Добавляем права в группу
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Группа "Moderators" успешно создана и права назначены'))
