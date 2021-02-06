from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group, User
from django.forms import TextInput, PasswordInput, EmailInput, DateTimeInput
from django.forms import ModelForm


class BasicSignupForm(SignupForm):

    def save(self, request):
        # Метод переопределяет форму регистрации через allauth. Достаем пользователя
        # из реквест, достаем группу common через гет, в эту группу добавляем 
        # пользователя
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user



class EditForm(ModelForm):
    """Форма редактирования профиля пользователя"""
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email',]

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'введите логин'
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ваше имя'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ваша фамилия'
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'адрес электронной почты'
            }),
        }