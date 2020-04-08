from django.contrib import admin
from .models import *

admin.site.register(UserProfile)

admin.site.register(Interests)

admin.site.register(Dialog)

admin.site.register(Message)

admin.site.register(MatchFriend)