from django import forms
from .models import Video


class VideoForm (forms.Form):

    class Meta:
        model = Video
        fields = "__all__"
