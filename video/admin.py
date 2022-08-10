from django.contrib import admin
from .models import Video, Category, Like, Comment, Profile
# Register your models here.


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'video')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'body')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', "school", "verified")
