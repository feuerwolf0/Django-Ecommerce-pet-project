from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .models import Profile


def create_profile(sender, instance, created, **kwargs):
    """
    Создает профиль когда создается User
    """
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )


post_save.connect(create_profile, sender=User)


def update_user(sender, instance, created, **kwargs):
    """
    Обновляет User когда обновляется Profile
    """
    if not created:
        profile = instance
        user = profile.user
        user.email = profile.email
        user.first_name = profile.first_name
        user.last_name = profile.last_name
        user.save()


post_save.connect(update_user, sender=Profile)
