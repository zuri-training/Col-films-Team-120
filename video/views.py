from django.shortcuts import render, redirect
from .models import Category, Video
from django.contrib.auth.decorators import login_required
from .forms import LikeForm, VideoForm
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from moviepy.editor import VideoFileClip


def landingView(request):
    return render(request, "video/landingpage.html", {})


def homeView(request):
    videos = Video.objects.all()
    bannerVid = videos.first()
    return render(request, "video/homepage.html", {"videos": videos, "bannerVid": bannerVid})


@login_required
def videoView(request, video_slug):
    video = Video.objects.get(slug=video_slug)
    relatedVideos = Video.objects.filter(
        category=video.category).exclude(id=video.id)
    return render(request, "video/single-video.html", {"video": video, "related": relatedVideos})


@login_required
def uploadVideoView(request):
    if(request.method == "POST"):
        form = VideoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save(commit=False)
            # return redirect("/accounts/profile")
        else:
            formData = form.errors.get_json_data()
            for err in formData:
                print(formData[err][0]["message"])
            return JsonResponse(formData)
    else:
        vidform = VideoForm()
        categories = Category.objects.all()
        return render(request, "video/upload-video.html", {"form": vidform, "categories": categories})


def LikeVideo(request, video_id):
    if request.method == "POST":
        form = LikeForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": "liked successfully"})
        else:
            return JsonResponse({"Unable to like"})
