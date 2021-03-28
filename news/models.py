from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache


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
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def get_category_label_list(self):
        for category in self.CATEGORIES:
            if category[0] == self.post_category:
                return category

    def get_subscribers_info_by_category(self):
        subscribers_info = []
        category_subscribers_objects = CategorySubscribers.objects.filter(category=self)
        if category_subscribers_objects.count():
            for category_subscribers_object in category_subscribers_objects:
                subscriber_info = {
                    'email': category_subscribers_object.user.email,
                    'name': category_subscribers_object.user.first_name or category_subscribers_object.user.username,
                    'category': self.get_category_label_list()[1]
                }
                subscribers_info.append(subscriber_info.copy())
        return subscribers_info

    def __str__(self):
        return self.get_category_label_list()[1]


class CategorySubscribers(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


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

    def get_categories(self):
        categories = []
        for post_category_obj in PostCategory.objects.filter(post=self):
            categories += [post_category_obj.category.get_category_label_list()]
        return categories

    def get_subscribers_info_by_post(self):
        subscribers_info = []
        for post_category_obj in PostCategory.objects.filter(post=self):
            category_subscribers_info = \
                post_category_obj.category.get_subscribers_info_by_category()
            if subscribers_info and category_subscribers_info:
                i = 0
                for existent_subscriber in subscribers_info:
                    for new_subscriber in category_subscribers_info:
                        if existent_subscriber['email'] == new_subscriber['email']:
                            subscribers_info[i]['category'] += ", " + new_subscriber['category']
                            category_subscribers_info.remove(new_subscriber)
                    i += 1
            subscribers_info += category_subscribers_info
        return subscribers_info

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # удаляем post из кэша, чтобы сбросить его
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    """Модель PostCategory
    Промежуточная модель для связи «многие ко многим»:
        связь «один ко многим» с моделью Post;
        связь «один ко многим» с моделью Category.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        for category in self.category.CATEGORIES:
            if category[0] == self.category.post_category:
                return f'self.post.id {category[1]}'


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
