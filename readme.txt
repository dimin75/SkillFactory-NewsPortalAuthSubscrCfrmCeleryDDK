Итоговое задание 10.5.1 (HW-03)
Новостной портал с проверкой прав доступа и возможностью ввода статей
разными пользователями. Добавления по заданию:
1. Redis установлен в wsl (ubunt-terminal).
2. Установлен Celery (venv pycharm)
3. Обновлена конфигурация settings.py, выполнение задач перенесено
   в tasks.py, добавлено расписание для celery (celery.py) для 
   запуска отправки еженедельного списка публикаций подписчикам. 
   Модифицирован views.py под использование с celery при отправке
   извещения о создании новой статьи.

Перед запуском:
pip install django
pip install django-filter
pip install django-allauth
pip install celery  
pip install redis 
pip install -U "celery[redis]"

или

pip install -r .\requirements.txt

запуск:
1. Сервер:
ython manage.py runserver 
2. Celery (в другом окне):
celery -A ddkNewsPortAuth worker -P threads

Настройка базы сообщений загрузкой статей и созданием пользователей:
пример в файле loading_news_base_users34.txt