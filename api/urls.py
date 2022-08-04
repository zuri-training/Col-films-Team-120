from django.urls import path
from .views import CategoryView, LoginView, VideoListView, VideoView, VideoDeleteView, CategoryListView

urlpatterns = [
    path('', VideoListView.as_view()),
    path('video/', VideoView.as_view()),
    path('video/<int:video_id>', VideoView.as_view()),
    path('delete-video/<pk>', VideoDeleteView.as_view()),
    path('login/', LoginView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('categories/new-category', CategoryView.as_view()),
    path('categories/<int:category_id>', CategoryView.as_view()),
]
