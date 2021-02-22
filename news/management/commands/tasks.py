from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.template.loader import render_to_string
from news.models import Post, Category
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


def weekly_news_notify():
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    all_weekly_news = Post.objects.filter(type='NW').filter(creation_datetime__gte=week_ago, creation_datetime__lt=now)
    for category in Category.objects.all():
        subscribers_info = category.get_subscribers_info_by_category()
        category_news = all_weekly_news.filter(category=category).order_by('-creation_datetime')
        print(f'si and new: {subscribers_info} {category_news}')
        if subscribers_info and category_news:
            for subscriber_info in subscribers_info:
                email = subscriber_info['email']
                name = subscriber_info['name']
                category_label = subscriber_info['category']
                html_content = render_to_string( 
                    'weekly_news_notify.html',
                    {
                        'news': category_news,
                        'name': name,
                        'category_label': category_label,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f'Новости портала np-d.test.com',
                    body=f'Здравствуйте, {name}. Новая статьи в категории {category_label}!',
                    from_email=settings.SERVER_EMAIL,
                    to=[email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()