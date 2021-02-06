from django.urls import path
from .views import UserProfile, become_author, EditProfile

urlpatterns = [
    path('<str:username>/', UserProfile.as_view(), name='profile'),
    path('<str:username>/upgrade', become_author, name='become_author'),
    path('<str:username>/edit', EditProfile.as_view(), name='edit_profile'),
]