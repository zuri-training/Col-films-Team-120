from django.forms import ModelForm
from .models import Like, Video


class VideoForm (ModelForm):

    class Meta:
        model = Video
        fields = '__all__'


class LikeForm(ModelForm):
    class Meta:
        model = Like
        fields = '__all__'
