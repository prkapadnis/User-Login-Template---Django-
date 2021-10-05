from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(
        default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} profile"


def profile_create(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(profile_create, sender=User)
