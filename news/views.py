# from django.shortcuts import render
from django.views.generic import ListView, DetailView
# импортируем класс, который говорит нам о том, что в этом представлении 
# мы будем выводить список объектов из БД
from .models import Post


class NewsList(ListView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут 
    # все инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'news.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, 
    # чтобы обратиться к самому списку объектов через html-шаблон
    context_object_name = 'news'
    queryset = Post.objects.filter(type='NW').order_by('-creation_datetime')


class OneNewsDetail(DetailView):
    # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    model = Post
    template_name = 'one_news.html' # название шаблона будет one_news.html
    context_object_name = 'one_news' # название объекта. в нём будет
    queryset = Post.objects.filter(type='NW')
