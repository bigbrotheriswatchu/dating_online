from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path("accounts/profile/", UserProfileDetailView.as_view(), name="profile_detail"),
    path("dating/", DatingListView.as_view(), name="get_profile_for_match"),
    path("accounts/profile/<int:pk>/profile_update/", UserProfileUpdateView.as_view(), name="profile_update"),
    path("accounts/profile/<int:pk>/user_update/", UserUpdateView.as_view(), name="user_update"),
    path("login/", login, name="login"),
    url(r"^like-request/like/(?P<pk>[\w-]+)/$", send_like_to_profile, name='like'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', send_skip_to_profile, name='skip_user'),
    #path("accounts/logout/", LogoutView.as_view(), name="logout"),
]
