from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from news.models import Post, Category
from django.core.mail import EmailMultiAlternatives
from celery import shared_task

def notify(subscriber_info, html_template, news):
    email = subscriber_info['email']
    name = subscriber_info['name']
    category_label = subscriber_info['category']
    html_content = render_to_string(
        html_template,
        {
            'news': news,
            'name': name,
            'category_label': category_label,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Новости портала np-d.test.com',
        body=f'Здравствуйте, {name}. Новые статьи в категории {category_label}!',
        from_email=settings.SERVER_EMAIL,
        to=[email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task
def weekly_news_notify():
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    all_weekly_news = Post.objects.filter(type='NW').filter(creation_datetime__gte=week_ago, creation_datetime__lt=now)
    for category in Category.objects.all():
        subscribers_info = category.get_subscribers_info_by_category()
        news = all_weekly_news.filter(category=category).order_by('-creation_datetime')
        if subscribers_info and news:
            for subscriber_info in subscribers_info:
                notify(subscriber_info, 'weekly_news_notify.html', news)

@shared_task
def news_notify(categories_names, post_id):
    for category_name in categories_names:
        subscribers_info = Category.objects.get(post_category=category_name).get_subscribers_info_by_category()
        new_post = Post.objects.get(id=post_id)
        if subscribers_info:
            for subscriber_info in subscribers_info:
                notify(subscriber_info, 'news_added.html', new_post)