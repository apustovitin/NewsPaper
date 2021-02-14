from django.forms import *
from .models import Post, Category, PostCategory
from accounts.models import Author


# Создаём модельную форму
class NewsForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма
    # и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    category = ModelMultipleChoiceField(queryset=Category.objects.all())
    class Meta:
        model = Post
        fields = ['title', 'type', 'category', 'content']