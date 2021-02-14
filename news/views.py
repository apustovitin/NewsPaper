from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# импортируем класс, который говорит нам о том, что в этом представлении 
# мы будем выводить список объектов из БД
from .models import Post, Category
# импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.core.paginator import Paginator
from .filters import NewsFilter # импортируем недавно написанный фильтр
from .forms import NewsForm # импортируем нашу форму
from django.contrib.auth.mixins import PermissionRequiredMixin
from accounts.models import Author
from django.shortcuts import redirect

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
    paginate_by = 3


class OneNewsDetail(DetailView):
    # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    model = Post
    template_name = 'one_news.html' # название шаблона будет one_news.html
    context_object_name = 'one_news' # название объекта. в нём будет
    queryset = Post.objects.filter(type='NW')


class NewsSearch(ListView):
    # указываем модель, объекты которой мы будем выводить
    model = Post
    # указываем имя шаблона, в котором будет лежать html, в котором будут 
    # все инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'news_search.html'
    # это имя списка, в котором будут лежать все объекты, его надо указать, 
    # чтобы обратиться к самому списку объектов через html-шаблон
    context_object_name = 'news_search'
    queryset = Post.objects.filter(type='NW').order_by('-creation_datetime')
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # забираем отфильтрованные объекты переопределяя метод get_context_data
        # у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsAdd(PermissionRequiredMixin, CreateView):
    ## дженерик для создания объекта. Надо указать только имя шаблона и класс формыс
    # указываем имя шаблона, в котором будет лежать html, в котором будут 
    # все инструкции о том, как именно пользователю должны вывестись наши объекты
    template_name = 'news_add.html'
    # добавляем форм класс, чтобы получать доступ к форме через метод POST
    form_class = NewsForm
    permission_required = ('news.add_post')

    def form_valid(self, form):
        new_post = form.save(commit=False)
        new_post.author = Author.objects.get(user=self.request.user)
        new_post.save()
        return redirect(f'/news/{new_post.id}/')


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    # дженерик для редактирования объекта
    template_name = 'news_add.html'
    form_class = NewsForm
    permission_required = ('news.change_post')

    def get_object(self, **kwargs):
        # метод get_object мы используем вместо queryset, чтобы получить 
        # информацию об объекте который мы собираемся редактировать
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    # дженерик для редактирования объекта
    template_name = 'news_delete.html'
    context_object_name = 'one_news'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = ('news.delete_post')