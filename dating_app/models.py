from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # choices for gender
    MALE    = 'M'
    FEMALE  = 'FM'
    UNKNOWN = 'UNKW'

    GENDERS = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
        (UNKNOWN, 'Неизвестно')
    )
    genders = models.CharField(max_length=10, choices=GENDERS, default=UNKNOWN)

    # head information about profile
    location = models.CharField(max_length=50)
    age = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
        ]

    about_me = models.TextField(max_length=300)
    avatar      =   models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


class Interests(models.Model):
    interests = models.ManyToManyField(UserProfile, blank=True)
    title = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title


class Dialog(models.Model):
    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Dialog owner", related_name="selfDialogs",
                              on_delete=models.CASCADE)
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Dialog opponent", on_delete=models.CASCADE)

    def __str__(self):
        return _("Chat with ") + self.opponent.username


class Message(models.Model):
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    dialog = models.ForeignKey(Dialog, verbose_name="Dialog", related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages",
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Message text")
    read = models.BooleanField(verbose_name="Read", default=False)
    pub_date = models.DateTimeField(auto_now_add=True)


class MatchFriend(models.Model):
    users = models.ManyToManyField(UserProfile)

    current_user = models.ForeignKey(UserProfile, related_name='owner',  on_delete=models.CASCADE, default=False)

    @classmethod
    def make_friend(cls, current_user, new_match_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_match_friend)

    @classmethod
    def lose_friend(cls, current_user, new_match_friend):
        friend, create = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_match_friend)