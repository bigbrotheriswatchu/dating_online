from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


def login(request):
    return render(request, 'registration/login.html')


class UserProfileDetailView(DetailView):
    Model = UserProfile
    template_name = 'dating_app/profile_detail.html'

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UserProfileUpdateView(UpdateView):
    template_name = 'dating_app/profile_update.html'
    model = UserProfile
    fields = '__all__'
    template_name_suffix = '_update'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)


class UserUpdateView(UpdateView):
    template_name = 'dating_app/user_form.html'
    model = User
    form_class = ExtendedUserCreationForm
    template_name_suffix = '_form'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)