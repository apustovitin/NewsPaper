from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Модель Category
    Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
    Имеет единственное поле: название категории.
    Поле должно быть уникальным (в определении поля необходимо написать параметр unique = True).
    """
    sport = 'SPT'
    politics = 'PLC'
    education = 'EDC'
    other = 'OTH'
    CATEGORIES = [
        (sport, 'спорт'),
        (politics, 'политика'),
        (education, 'образование'),
        (other, 'другое')
    ]
    post_category = models.CharField(max_length=3, choices=CATEGORIES, default=other, unique=True)

    def __str__(self):
        for category in self.CATEGORIES:
            if category[0] == self.post_category:
                return f'{category[1]}'


class Post(models.Model):
    """Модель Post
    Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
    Каждый объект может иметь одну или несколько категорий.
    Соответственно, модель должна включать следующие поля:
        связь «один ко многим» с моделью Author;
        поле с выбором — «статья» или «новость»;
        автоматически добавляемая дата и время создания;
        связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
        заголовок статьи/новости;
        текст статьи/новости;
        рейтинг статьи/новости.
    """
    article = 'AT'
    news = 'NW'
    TYPES = [(article, 'статья'), (news, 'новость')]
    author = models.ForeignKey('accounts.Author', on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=news)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        """ Метод увеличивает рейтинг поста на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """ Метод уменьшает рейтинг поста на единицу."""
        self.rating -= 1
        self.save()

    def preview(self):
        """возвращает начало статьи (предварительный просмотр)
        длиной 124 символа и добавляет многоточие в конце.
        """
        return self.content[:124] + "..."

    def get_absolute_url(self):
        # добавим абсолютный путь чтобы после создания нас перебрасывало 
        # на страницу с новостью
        return f'/news/{self.id}' 


class PostCategory(models.Model):
    """Модель PostCategory
    Промежуточная модель для связи «многие ко многим»:
        связь «один ко многим» с моделью Post;
        связь «один ко многим» с моделью Category.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    """Модель Comment
    Под каждой новостью/статьей можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
    Модель будет иметь следующие поля:
        связь «один ко многим» с моделью Post;
        связь «один ко многим» с встроенной моделью User
        (комментарии может оставить любой пользователь, не обязательно автор);
        текст комментария;
        дата и время создания комментария;
        рейтинг комментария.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        """ Метод увеличивает рейтинг комментария на единицу."""
        self.rating += 1
        self.save()

    def dislike(self):
        """ Метод уменьшает рейтинг комментария на единицу."""
        self.rating -= 1
        self.save()
