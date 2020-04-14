from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, ListView

from django.contrib.auth.models import User
from django.views.generic.edit import FormMixin

from .forms import ExtendedUserCreationForm, UserProfileForm
from .models import UserProfile, MatchFriend


def login(request):
    return render(request, 'registration/login.html')


# showing user profile

class UserProfileDetailView(LoginRequiredMixin, DetailView):
    Model = UserProfile
    template_name = 'dating_app/profile_detail.html'
    success_url = "/accounts/profile/"

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)


# user profile edition
class UserProfileUpdateView(UpdateView):
    template_name = 'dating_app/profile_update.html'
    model = UserProfile
    # fields = ['genders', 'age', 'location', 'about_me', 'avatar']
    form_class = UserProfileForm
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


class DatingListView(ListView):
    # queryset = UserProfile.objects.filter()
    model = UserProfile
    template_name_suffix = 'dating.html'
    template_name = 'dating_app/dating.html'
    paginate_by = 1

    def get_queryset(self):
        profile = self.request.user.userprofile
        skip_pk = profile.skip_ids.values_list('pk', flat=True)
        like_pk = profile.like_ids.values_list('pk', flat=True)
        return UserProfile.objects.filter(age__lte=profile.to_age,
                                          age__gte=profile.from_age,
                                          genders=profile.gender_pref).exclude(pk__in=skip_pk).exclude(pk__in=like_pk)


# function for like in /dating/ page
def send_like_to_profile(request, pk):
    if request.user.is_authenticated:
        user = request.user.userprofile
        profile = get_object_or_404(UserProfile, pk=pk)
        like_request, created = MatchFriend.objects.get_or_create(
            current_user=request.user.userprofile,
            users=profile, is_like=True,
        )
        user.like_ids.add(profile)
        return HttpResponseRedirect('/dating/')


# function for skip in /dating/ page
def send_skip_to_profile(request, operation, pk):
    if operation == 'skip':
        user = request.user.userprofile
        skip_user = get_object_or_404(UserProfile, pk=pk)
        user.skip_ids.add(skip_user)
        return HttpResponseRedirect('/dating/')
