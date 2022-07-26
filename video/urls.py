from django.urls import path
from .views import CommentVideo, LikeVideo, homeView, landingView, uploadVideoView, videoDataView, videoView
urlpatterns = [
    path('', landingView, name="landingpage"),
    path('homepage/', homeView, name="homepage"),
    path('videos/comment-video/', CommentVideo, name="comment-video"),
    path('videos/video-data/', videoDataView, name="video-data"),
    path('videos/upload-video/', uploadVideoView, name="upload-video"),
    path('videos/like/', LikeVideo, name="like-video"),
    path('videos/<slug:video_slug>/', videoView, name="single-video"),
]
