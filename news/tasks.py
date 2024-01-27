from celery import shared_task
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import CategorySubscribers, Post
from datetime import datetime, timedelta

#Уведомление о создании новой статьи
@shared_task
def new_post_notification(subj, email, content):
    time.sleep(5)
    emailfrom = 'dimatest24@yandex.ru'

    try:
        msg = EmailMultiAlternatives(
            subject=subj,
            body='',
            from_email=emailfrom,
            to=[email],
        )
        msg.attach_alternative(content, "text/html")
        msg.send()
        print('message from celery task: письмо успешно отправлено.')
    except Exception as e:
        print(f'Error sending email: {e}')

@shared_task
def weekly_notification():
    print("----------------------------------------------------------------------------------------------------------------------")
    if CategorySubscribers.objects.all().exists():
        subscribers = CategorySubscribers.objects.all()
        for subscriber in subscribers:
            user = subscriber.user
            print(user)
            subject = f'Здравствуй, {user}! Еженедельная рассылка новостей по категории "{subscriber.category}"'
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            posts_last_week = Post.objects.filter(created_at__range=(start_date, end_date))
            print('Last week posts:')
            for post in posts_last_week:
                print(post.title, post.created_at, subscriber.category)
            postList = posts_last_week
            html_content = render_to_string('subscribepostlist.html', {'postList': postList, })
            print('mail sent ok.')
            msg = EmailMultiAlternatives(
                subject=subject,
                body=html_content,
                from_email='dimatest24@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print('message from celery task: список статей успешно отправлен.')

