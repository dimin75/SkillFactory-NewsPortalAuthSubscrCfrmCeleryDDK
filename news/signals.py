# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.conf import settings
# from django.db import models
# from django.db.models.signals import post_save
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.core.mail import mail_managers
from django_apscheduler.jobstores import DjangoJobStore #, register_events
from django_apscheduler.models import DjangoJobExecution
from apscheduler.schedulers.background import BackgroundScheduler

from .models import Post, CategorySubscribers
from django_apscheduler import util
from datetime import datetime, timedelta

from django.utils import timezone

from django.core.exceptions import ValidationError

# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")
#register_events(scheduler)

# @receiver(post_save, sender=Post)
# def notify_news_creator(sender, instance, created, **kwargs):
#     if created:
#         print('hello from receiver: ')
#         author = getattr(instance, 'author', None)
#         if author and hasattr(author, 'user') and hasattr(author.user, 'email'):
#             print('отправляем письмо создателю новости:')
#             print(instance.title)
#             print('создал новость:')
#             print(author.user)
#             post = instance
#             subject = f'{instance.created_at.strftime("%Y-%M-%d")} вами создана новая новость!'
#             content = render_to_string('post_created_notification.html', {'post': post, })
#             email = 'dimatest24@yandex.ru'
#             try:
#                 msg = EmailMultiAlternatives(
#                     subject=subject,
#                     body=content,
#                     from_email=email,
#                     to=[instance.author.user.email],
#                 )
#                 msg.attach_alternative(content, "text/html")
#                 msg.send()
#                 print('письмо успешно отправлено.')
#             except Exception as e:
#                 print(f'Error sending email: {e}')
#         else:
#             print('Content suggestion not available')
#     else:
#         subject = f'Отредактирована новость: {instance.title}'
#         print(subject)

# @util.close_old_connections
# def ten_minute_notification():
#     print("----------------------------------------------------------------------------------------------------------------------")
#     if CategorySubscribers.objects.all().exists():
#         subscribers = CategorySubscribers.objects.all()
#         for subscriber in subscribers:
#             user = subscriber.user
#             print('Process user:')
#             print(user)
#             subject = f'Здравствуй, {user}! Еженедельная рассылка новостей по категории "{subscriber.category}"'
#             end_date = datetime.now()
#             start_date = end_date - timedelta(days=7)
#             posts_last_week = Post.objects.filter(created_at__range=(start_date, end_date))
#             print('Last week posts:')
#             for post in posts_last_week:
#                 print(post.title, post.created_at, subscriber.category)
#             postList = posts_last_week
#             html_content = render_to_string('subscribepostlist.html', {'postList': postList, })
#             print('mail sent ok.')
#             msg = EmailMultiAlternatives(
#                 subject=subject,
#                 body=html_content,
#                 from_email='dimatest24@yandex.ru',
#                 to=[user.email],
#             )
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#
