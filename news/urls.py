from django.urls import path
# импортируем наше представление
from .views import NewsList, OneNewsDetail, NewsSearch

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется 
    # пустым, позже станет ясно почему
    path('', NewsList.as_view()),
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view
    # pk — это первичный ключ поста, который будет выводиться у нас в шаблон
    path('<int:pk>', OneNewsDetail.as_view()),
    path('search', NewsSearch.as_view()),
]