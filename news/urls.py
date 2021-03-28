from django.urls import path
# импортируем наше представление
from .views import NewsList, OneNewsDetail, NewsSearch, NewsAdd, NewsUpdate, NewsDelete, \
    CategorizedNewsList, subscribe_category, unsubscribe_category
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path — означает путь.
    path('', cache_page(60)(NewsList.as_view())),
    path('<int:pk>/', OneNewsDetail.as_view(), name='one_news'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('add/', NewsAdd.as_view(), name='news_add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('<str:post_category>/', cache_page(60*5)(CategorizedNewsList.as_view()), name='categorized_news'),
    path('<str:post_category>/subscribe', subscribe_category, name='subscribe_category'),
    path('<str:post_category>/unsubscribe', unsubscribe_category, name='unsubscribe_category'),
]