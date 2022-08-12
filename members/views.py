from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from video.models import Video
# Create your views here.


def registerView(request):
    form = RegistrationForm()

    print("hello")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        # print(form.data)
        if form.is_valid():
            form.save()
            return JsonResponse({"success": "user registered successfully"})
        else:
            formData = form.errors.get_json_data()
            for err in formData:
                print(formData[err][0]["message"])
            return JsonResponse(formData)

    return render(request, "registration/register.html", {"form": form})


@login_required
def profileView(request):
    myVideos = Video.objects.filter(author=request.user).order_by("-id")
    return render(request, "registration/profile.html", {"myVideos": myVideos})
