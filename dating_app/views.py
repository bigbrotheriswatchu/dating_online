from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView

from django.contrib.auth.models import User
from .forms import ExtendedUserCreationForm, UserProfileForm
from .models import UserProfile


def login(request):
    return render(request, 'registration/login.html')


# showing user profile
class UserProfileDetailView(LoginRequiredMixin, DetailView):
    Model = UserProfile
    template_name = 'dating_app/profile_detail.html'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


# user profile edition
class UserProfileUpdateView(UpdateView):
    template_name = 'dating_app/profile_update.html'
    model = UserProfile
    fields = ['genders', 'age', 'location', 'about_me', 'avatar']
    # template_name_suffix = '_update'
    success_url = "/accounts/profile/"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


# user edition (password, login...)
class UserUpdateView(UpdateView):
    template_name = 'dating_app/user_form.html'
    model = User
    form_class = ExtendedUserCreationForm

    # template_name_suffix = '_form'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
