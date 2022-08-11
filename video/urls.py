from django.urls import path
from .views import homeView, landingView, videoView
urlpatterns = [
    path('', landingView, name="landingpage"),
    path('/homepage', homeView, name="homepage"),
    path('videos/<slug:video_slug>', videoView, name="single-video")
]
