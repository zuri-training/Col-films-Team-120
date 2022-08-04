from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Custom Imports
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, ** kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()
