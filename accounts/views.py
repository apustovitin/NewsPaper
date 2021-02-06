from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditForm
from django.urls import reverse


@login_required
def become_author(*args, **kwargs):
    username = kwargs.get('username')
    user = User.objects.get(username=username)
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/accounts/{username}/')


# Редактирование профиля
class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = EditForm
    template_name = 'accounts/edit_profile.html'
    login_url = '/accounts/login/'

    def get_object(self, **kwargs):
        username = self.kwargs.get('username')
        return User.objects.get(username=username)

    def get_success_url(self):
        return reverse('profile',  kwargs={'username': self.kwargs.get('username')})


class UserProfile(LoginRequiredMixin, ListView):
    """Представление страницы пользователя"""
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        context['user'] = User.objects.get(username=self.request.user)
        return context

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)
