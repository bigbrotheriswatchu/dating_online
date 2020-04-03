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
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    age = models.PositiveIntegerField(default=18)
    about_me = models.TextField(max_length=300)

    # choice interests for profile
    MOVIE       =   'MOVIES'
    TRAVELING   =   'TRAVEL'
    CARS        =   'CARS'
    BOOKS       =   'BOOKS'
    MUSIC       =   'MUSIC'
    DRAWING     =   'DRAW'

    INTERESTS = (
        (MOVIE, 'Фильмы'),
        (TRAVELING, 'Путешествия'),
        (CARS, 'Машины'),
        (BOOKS, 'Книги'),
        (MUSIC, 'Музыка'),
        (DRAWING, 'Рисование'),
    )
    interests = models.CharField(max_length=20, blank=True, choices=INTERESTS, default=None)

    avatar      =   models.ImageField(upload_to='profile_image', blank=True)
    is_online   =   models.BooleanField()

    def __str__(self):
        return self.first_name + self.last_name


class Dialog(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog owner"), related_name="selfDialogs",
                              on_delete=models.CASCADE)
    opponent = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Dialog opponent"), on_delete=models.CASCADE)

    def __str__(self):
        return _("Chat with ") + self.opponent.username


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, verbose_name=_("Dialog"), related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Author"), related_name="messages",
                               on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("Message text"))
    read = models.BooleanField(verbose_name=_("Read"), default=False)


class Friend(models.Model):
    users = models.ManyToManyField(User)

    current_user = models.ForeignKey(User, related_name='owner',  on_delete=models.CASCADE, default=False)

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