from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *


def login(request):
    return render(request, 'registration/login.html')


class UserProfileUpdateView(UpdateView):
    template_name = 'dating_app/profile.html'
    form_class = UserProfileForm
    queryset = UserProfile.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(UserProfile, id=id_)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)