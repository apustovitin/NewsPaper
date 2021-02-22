from django.urls import path
# импортируем наше представление
from .views import NewsList, OneNewsDetail, NewsSearch, NewsAdd, NewsUpdate, NewsDelete, \
    CategorizedNewsList, subscribe_category, unsubscribe_category

urlpatterns = [
    # path — означает путь.
    path('', NewsList.as_view()),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    # pk — это первичный ключ поста, который будет выводиться у нас в шаблон
    path('<int:pk>/', OneNewsDetail.as_view(), name='one_news'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('add/', NewsAdd.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('<str:post_category>/', CategorizedNewsList.as_view(), name='categorized_news'),
    path('<str:post_category>/subscribe', subscribe_category, name='subscribe_category'),
    path('<str:post_category>/unsubscribe', unsubscribe_category, name='unsubscribe_category'),
]