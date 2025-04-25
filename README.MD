Запуск проекта через Docker Compose

Убедитесь, что на вашем компьютере установлены Docker и Docker Compose.

В корне проекта находится файл docker-compose.yml.

Запустите все сервисы командой:
docker-compose up -d

Проверьте, что контейнеры запущены:
docker-compose ps

Для просмотра логов используйте:
docker-compose logs -f

Чтобы остановить и удалить контейнеры, выполните:
docker-compose down