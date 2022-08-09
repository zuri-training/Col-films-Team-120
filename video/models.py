from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
# Create your models here.

from members.models import Member


class Profile(models.Model):
    # User profile

    user = models.OneToOneField(
        Member, verbose_name=_("Member"), on_delete=models.CASCADE)
    school = models.CharField(
        _("School"), max_length=50, null=True, blank=True)
    verified = models.BooleanField(_("Verified"), default=False, blank=True)

    def __str__(self):
        return "{}'s Profile".format(self.user.username)

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"pk": self.pk})


class Category(models.Model):
    '''
        Category model to enable users add category
    '''

    title = models.CharField(_("Title"), max_length=50)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.title


class Video(models.Model):
    # Video model

    author = models.ForeignKey(
        Member, verbose_name=_("Author"), on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=50, unique=True)
    description = models.TextField(_("Description"))
    video_file = models.FileField(
        _("Video"), upload_to="videos/%Y/%m", max_length=100, blank=True, validators=[FileExtensionValidator(['mp4'])])
    categories = models.ManyToManyField(Category, verbose_name=_("Categories"))
    published = models.BooleanField(_("Published"), default=False, blank=True)

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __str__(self):
        return self.title


class Like(models.Model):
    # Like and dislike

    user = models.ForeignKey(Member, verbose_name=_(
        "User"), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name=_(
        "Video"), on_delete=models.CASCADE)
    liked = models.BooleanField(_("Liked"), null=True, blank=True)

    def __str__(self):
        if self.liked:
            return "{} liked {}".format(self.user.username, self.video.title)
        return "{} disliked {}".format(self.user.username, self.video.title)


class Comment(models.Model):
    # Comment model
    user = models.ForeignKey(Member, verbose_name=_(
        "user"), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name=_(
        "Video"), on_delete=models.CASCADE)
    body = models.TextField(_("Message"))

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return "{} made a comment on {}".format(self.user.username, self.video.title)


class ScheduledUpload(models.Model):

    video = models.OneToOneField(
        Video, verbose_name=_("Video"), on_delete=models.CASCADE)
    expires = models.DateTimeField(_("Expires"))
    expired = models.BooleanField(_("Expired"), default=False)

    def __str__(self):
        return self.expires
