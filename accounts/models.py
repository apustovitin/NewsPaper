from django.db import models
from django.contrib.auth.models import User
from news.models import Post, Comment


class Author(models.Model):
    """Модель Author
    Модель, содержащая объекты всех авторов.
    Имеет следующие поля:
        cвязь «один к одному» с встроенной моделью пользователей User;
        рейтинг пользователя.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def _update_posts_rating(self):
        """Возвращает суммарный рейтинг каждой статьи автора умноженный на 3."""
        common_posts_rating = 0
        posts = Post.objects.filter(author__user=self.user)
        if posts.exists():
            for individual_post_rating in posts.values("rating"):
                common_posts_rating += individual_post_rating["rating"] * 3
        return common_posts_rating

    def _update_posts_comments_rating(self):
        """Возвращает суммарный рейтинг всех комментариев к статьям автора
        без учета комментариев автора к своим статьям.
        """
        common_posts_comments_rating = 0
        all_posts_comments = Comment.objects.filter(post__author__user=self.user).exclude(
            user=self.user)
        if all_posts_comments.exists():
            for individual_comment_rating in all_posts_comments.values("rating"):
                common_posts_comments_rating += individual_comment_rating["rating"]
        return common_posts_comments_rating

    def _update_author_comments_rating(self):
        """Возвращает суммарный рейтинг всех комментариев автора."""
        common_author_comments_rating = 0
        all_author_comments = Comment.objects.filter(user=self.user)
        if all_author_comments.exists():
            for individual_comment_rating in all_author_comments.values("rating"):
                common_author_comments_rating += individual_comment_rating["rating"]
        return common_author_comments_rating

    def update_rating(self):
        """Метод update_rating() модели Author, который обновляет рейтинг пользователя,
        переданный в аргумент этого метода.
        Он состоит из следующего:
            суммарный рейтинг каждой статьи автора умножается на 3;
            суммарный рейтинг всех комментариев автора;
            суммарный рейтинг всех комментариев к статьям автора.
        """
        self.rating = self._update_author_comments_rating() + self._update_posts_comments_rating() \
                      + self._update_posts_rating()
        self.save()
