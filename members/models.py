from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# Create your models here.


class MemberManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, school, grad_year, password, username, **other_fields):

        if not email:
            raise ValueError("Email field is required")

        if not username:
            raise ValueError("The username field is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name,
                          last_name=last_name, school=school, grad_year=grad_year, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, username,  **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        # user_name = "superuser"

        if other_fields.get('is_staff') is not True:
            raise ValueError("superuser must be a staff")
        if other_fields.get('is_superuser') is not True:
            raise ValueError("superuser must be set to true")
        return self.create_user(email=email, password=password, username=username, **other_fields)


class Member(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    username = models.CharField(
        _("Username"), max_length=50, unique=True, null=True)
    first_name = models.CharField(_("Firstname"), max_length=50)
    last_name = models.CharField(_("Lastname"), max_length=50)
    start_date = models.DateTimeField(_("Registered"), default=timezone.now)
    about = models.TextField(_("About"), max_length=500, blank=True)
    school = models.CharField(_("School"), max_length=50)
    is_staff = models.BooleanField(_("Staff"), default=False)
    is_active = models.BooleanField(_("Active"), default=False)
    is_superuser = models.BooleanField(_("Superuser"), default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name', 'school']

    def __str__(self):
        return self.email
