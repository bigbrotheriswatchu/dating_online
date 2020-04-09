from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path("accounts/profile/", UserProfileDetailView.as_view(), name="profile_detail"),
    path("accounts/profile/<int:pk>/profile_update/", UserProfileUpdateView.as_view(), name="profile_update"),
    path("accounts/profile/<int:pk>/user_update/", UserUpdateView.as_view(), name="user_update"),
    path("login/", login, name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
]
