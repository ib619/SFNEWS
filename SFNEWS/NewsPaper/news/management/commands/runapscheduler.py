import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

# importing models
from django.contrib.auth.models import User
from news.models import Category, Post
import datetime as DT

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


# my custom task
def my_job():
    print("started job")
    # load all category objects
    categories = Category.objects.all()

    # iterate through categories
    for category in categories:
        print('entered category loop')
        # load posts ordered by date
        all_posts = Post.objects.filter(category=category).order_by('-date')
        length = len(all_posts)
        post_list = []
        for i in range(length):
            week_ago = DT.date.today() - DT.timedelta(days=7)
            condition = all_posts[i].date.date() > week_ago
            if condition:
                post_list.append(all_posts[i])
            else:
                break

        for post in post_list:
            print(f'{category.name}: {post.name}, {post.date}')

        # load all category subscribers
        subs = category.subscribers.all()
        for sub in subs:
            print('entered sub loop')
            html_content = render_to_string(
                'weekly_mail.html',
                {
                    'posts': post_list,
                    'sub_name': sub.username,
                    'category_name': category.name,
                }
            )

            msg = EmailMultiAlternatives(
                subject="Here's whats you've missed this week",
                body=f'Hello, {sub.username}! These are the posts in you favourite category {category.name} from last week. Enjoy!',
                from_email='igorbodnarprog@yandex.ru',
                to=[sub.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=True)


def delete_old_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apsheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )

        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting sheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            logger.info("Scheduler shut down succefully!")


