import sched
from django import forms
from .models import Member
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label="Email", max_length=100, required=True)
    username = forms.CharField(label="Username", max_length=100, required=True)
    first_name = forms.CharField(
        label="First Name", max_length=100, required=True)
    last_name = forms.CharField(
        label="Last Name", max_length=100, required=True)
    school = forms.CharField(label="School", max_length=100, required=True)

    class Meta:
        model = Member
        fields = ("email",   "username", "first_name", "last_name", "school")
        # fields = "__all__"

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.school = self.cleaned_data["school"]
        if commit:
            user.save()
        return user
