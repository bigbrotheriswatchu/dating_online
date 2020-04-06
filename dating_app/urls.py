from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path("<int:id>/profile/", UserProfileUpdateView.as_view(), name="profile_update"),
    path("login/", login, name="login"),
    #path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
