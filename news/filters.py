from django_filters import *
from .models import Post


class NewsFilter(FilterSet):
    creation = DateTimeFilter(field_name='creation_datetime', lookup_expr='gt')
    title = CharFilter(lookup_expr='icontains')
    class Meta:
        model = Post
        fields = ['creation', 'author__user', 'title']