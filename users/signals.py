from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save

from fifa_draft.models import Profile


def create_profile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user, username=user.username, email=user.email, name=user.first_name
        )
        subject = "Welcome to Fifa draft page!"
        message = "We are glad you are here!"
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()


def update_user(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


post_save.connect(create_profile, sender=User)
post_delete.connect(delete_profile, sender=Profile)
post_save.connect(update_user, sender=Profile)
