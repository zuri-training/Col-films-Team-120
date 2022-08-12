from django.urls import path
from .views import homeView, landingView, uploadVideoView, videoView
urlpatterns = [
    path('', landingView, name="landingpage"),
    path('homepage/', homeView, name="homepage"),
    path('videos/upload-video/', uploadVideoView, name="upload-video"),
    path('videos/<slug:video_slug>/', videoView, name="single-video"),
]
