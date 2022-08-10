from django.urls import path
from .views import (
    CategoryView, CommentView, ProfileView,
    RegisterView, VideoListView, VideoView, CategoryListView,
    LikeView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # VIDEO ENDPOINTS
    path('', VideoListView.as_view()),
    path('video/', VideoView.as_view()),
    path('video/<slug:video_slug>', VideoView.as_view()),

    # USER ENDPOINTS
    # path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    # path('logout/', LogoutView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

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
