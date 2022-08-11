from django.shortcuts import render, redirect
from .models import Video
# from django.contrib.auth.forms import UserCreationForm


def landingView(request):
    return render(request, "video/landingpage.html", {})


def homeView(request):
    videos = Video.objects.all()
    bannerVid = videos.first()
    return render(request, "video/homepage.html", {"videos": videos, "bannerVid": bannerVid})


def videoView(request, video_slug):
    video = Video.objects.get(slug=video_slug)
    relatedVideos = Video.objects.filter(
        category=video.category).exclude(id=video.id)
    return render(request, "video/single-video.html", {"video": video, "related": relatedVideos})

# def uploadVideoView(request):
#     form =
