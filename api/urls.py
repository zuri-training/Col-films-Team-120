from django.urls import path
from .views import (
    CategoryView, CommentView, LoginView, LogoutView, ProfileView,
    RegisterView, VideoListView, VideoView, CategoryListView,
    LikeView
)

urlpatterns = [
    # VIDEO ENDPOINTS
    path('', VideoListView.as_view()),
    path('video/', VideoView.as_view()),
    path('video/<int:video_id>', VideoView.as_view()),

    # USER ENDPOINTS
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('logout/', LogoutView.as_view()),

    # CATEGORIES ENDPOINTS
    path('categories/', CategoryListView.as_view()),
    path('categories/new-category', CategoryView.as_view()),
    path('categories/<int:category_id>', CategoryView.as_view()),

    # LIKES ENDPOINTS
    path('likes/', LikeView.as_view()),
    path('likes/<int:video_id>', LikeView.as_view()),

    # COMMENTS ENDPOINTS
    path('comments/', CommentView.as_view()),
    path('comments/<int:video_id>', CommentView.as_view()),

    # PROFILE ENDPOINTS
    path('profile/', ProfileView.as_view()),
]
