from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post
import datetime as DT
from django.contrib.auth.models import User


@shared_task
def send_notification(post_id):
    post = Post.objects.get(pk=post_id)
    cats = post.category.all()
    for cat in cats:
        subs = cat.subscribers.all()
        for sub in subs:
            html_content = render_to_string(
                'post_create_celery_mail.html',
                {
                    'post': post,
                    'sub_name': sub.username,
                }
            )
            msg = EmailMultiAlternatives(
                subject=f'{post.name}',
                body=f'Hello, {sub.username}. New post in your favourite category!',
                from_email='igorbodnarprog@yandex.ru',
                to=[sub.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)


@shared_task
def latest_news():
    all_posts = Post.objects.all().order_by('-date')
    length = len(all_posts)
    post_list = []

    all_users = User.objects.all()

    for i in range(length):
        week_ago = DT.date.today() - DT.timedelta(days=7)
        condition = all_posts[i].date.date() > week_ago
        if condition:
            post_list.append(all_posts[i])
        else:
            break

    for user in all_users:
        html_content = render_to_string(
            'celery_weekly_mail.html',
            {
                'posts': post_list,
                'sub_name': user.username,
            }
        )

        msg = EmailMultiAlternatives(
            subject="Here's whats you've missed this week",
            body=f'Hello, {user.username}! These are the posts you missed last week!',
            from_email='igorbodnarprog@yandex.ru',
            to=[user.email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)

