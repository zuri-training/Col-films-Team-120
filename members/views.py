from django.shortcuts import render, redirect
from .forms import RegistrationForm
# Create your views here.


def registerView(request):
    form = RegistrationForm()

    print("hello")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        # print(form)
        if form.is_valid():
            form.save()
            return redirect("/")
        else:
            form = RegistrationForm()
            context = {
                "form": form,
                "errors": form.errors
            }
            return render(request, "registration/register.html", context)

    return render(request, "registration/register.html", {"form": form})
