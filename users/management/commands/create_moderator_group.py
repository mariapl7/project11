from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Создание группы модераторов'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор" создана'))
        else:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор" уже существует'))
