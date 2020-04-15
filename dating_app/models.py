from django.conf import settings
from django.db import models
from sorl.thumbnail import ImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # choices for gender
    MALE = 'Мужчина'
    FEMALE = 'Женщина'
    UNKNOWN = 'Неизвестно'

    GENDERS = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
        (UNKNOWN, 'Неизвестно')
    )
    genders = models.CharField(max_length=10, choices=GENDERS, default=UNKNOWN)

    # head information about profile
    location = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(default=18)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
        ]

    about_me = models.TextField(max_length=300, blank=True)
    avatar = ImageField(upload_to='profile_image', blank=True)

    # like and skip
    skip_ids = models.ManyToManyField("UserProfile", blank=True, related_name='skip_id')
    like_ids = models.ManyToManyField("UserProfile", blank=True, related_name='like_id')
    #preferences
    from_age = models.PositiveIntegerField(default=18)
    to_age = models.PositiveIntegerField(default=18)
    gender_pref = models.CharField(max_length=10, choices=GENDERS, default=UNKNOWN)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


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
        return "Chat with " + self.opponent.username


class Message(models.Model):
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    dialog = models.ForeignKey(Dialog, verbose_name="Dialog", related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Author", on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Message text")
    read = models.BooleanField(verbose_name="Read", default=False)
    pub_date = models.DateTimeField(auto_now_add=True)


class MatchFriend(models.Model):
    users = models.ForeignKey(UserProfile, related_name='to_user', on_delete=models.CASCADE, default=False)
    current_user = models.ForeignKey(UserProfile, related_name='form_user', on_delete=models.CASCADE, default=False)
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return self.current_user.user.first_name +' '+ self.current_user.user.last_name


