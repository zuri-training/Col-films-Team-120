from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):
    title = models.CharField(_("Title"), max_length=50)


class Video(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"))
    # Add a few installs Pillow, setup static files upload
    categories = models.ManyToManyField(Category, verbose_name=_(
        "Categories"))
    author = models.ForeignKey(User, verbose_name=_(
        "Author"), on_delete=models.CASCADE)
    likes = models.PositiveIntegerField(_("Likes"))
    created_at = models.TimeField(_("Created"), auto_now=False)
    timer_set = models.BooleanField(_("Timer Set"))
    published = models.BooleanField(_("Published"))


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name=_(
        "Video"), on_delete=models.CASCADE)
    body = models.TextField(_("Body"))


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name=_(""),
                             on_delete=models.CASCADE)
    school = models.CharField(_("School"), max_length=50)
    created_at = models.TimeField(_("Created"), auto_now=False)
    uploaded_videos = models.ForeignKey(
        Video, verbose_name=_("Video"), on_delete=models.CASCADE)
    comments = models.ForeignKey(Comment, verbose_name=_(
        "Comments"), on_delete=models.CASCADE)
    verified = models.BooleanField(_("Verified"))


class UploadSchedule(models.Model):
    time = models.TimeField(_("Time Due"))
    disable_timer = models.BooleanField(_("Disabled"))
    time_elapsed = models.BooleanField(_("Elapsed"))
