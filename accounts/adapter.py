from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter, get_account_adapter
from django.contrib.auth.models import Group, User

class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/accounts/{username}/"
        return path.format(username=request.user.username)


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def save_user(self, request, sociallogin, form=None):
        # с помощью super выполняем свой код библиотеки, и дальнее добавим свой
        user = super(SocialAccountAdapter,self).save_user(request, sociallogin, form=None)
        # Вытаскиваем из бд группу common и прикрепляем к нему нового пользователя
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
