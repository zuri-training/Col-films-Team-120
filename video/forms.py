from django.forms import ModelForm, HiddenInput
from .models import Like, Video


class VideoForm (ModelForm):

    class Meta:
        model = Video
        fields = '__all__'
        widgets = {'author': HiddenInput(), "slug": HiddenInput(),
                   "published": HiddenInput()}


class LikeForm(ModelForm):
    class Meta:
        model = Like
        fields = '__all__'
