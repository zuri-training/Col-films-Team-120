from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import jwt
import datetime
from django.conf import settings

# Custom imports
from .serializers import CategorySerializer, CommentSerializer, LikeSerializer, ProfileSerializer, UserSerializer, VideoSerializer
from video.models import Category, Comment, Like, Profile, Video
from .functions import authenticate_user, is_authenticated


class VideoListView(generics.ListAPIView):
    '''
    List all videos in the database
    '''

    queryset = Video.objects.filter(published=True)
    serializer_class = VideoSerializer


class VideoView(APIView):
    '''
        Actions to be performed on a single video instance

        1. GET: Get a single Video instance
        2.  POST: Create a new Video
        3. PUT: Update an existing video

    '''

    def get_object(self, video_id):
        '''
            Get a single video instance by passing the video id
        '''
        try:
            return Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            raise Http404

    def get(self, request, video_id):
        '''
            REturn a single video instance to the api response
        '''
        video = self.get_object(video_id)
        serializer = VideoSerializer(video)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
            Upload a new video
        '''

        # Get user token from browser cookie
        jwt_token = request.COOKIES.get('user-token')

        # Authenticate user via cookie
        payload = authenticate_user(jwt_token)

        # Get user associated with token
        user = User.objects.filter(id=payload["id"]).first()

        # Create dictionary for video data before serializing
        video_data = {
            "author": user.id,
            "title": request.data["title"],
            "description": request.data["description"],
            "video_file": request.data["video_file"],
            "categories": [int(request.data["categories"]), ],
            "published": bool(request.data["published"])
        }

        serializer = VideoSerializer(data=video_data)

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Video Created"}, status=status.HTTP_201_CREATED)

        return Response({"detail": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, video_id):
        '''
            Update an Exisiting video associated with the video id passed with request
        '''
        # Get user token from cookie
        jwt_token = request.COOKIES.get('user-token')
        # Authenticate user with token
        payload = authenticate_user(jwt_token)

        if payload is not None:
            video = self.get_object(video_id)
            video_data = {
                "author": payload['id'],
                "title": request.data["title"],
                "description": request.data["description"],
                "categories": [int(x) for x in request.data["categories"].split(",")],
                "published": bool(int(request.data["published"])),
            }

            serializer = VideoSerializer(video, data=video_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, video_id):
        '''
        This delete view enables authenticated users to delete vidoes
        '''

        jwt_token = request.COOKIES.get('user-token')
        # Authenticate user with token
        payload = authenticate_user(jwt_token)

        if payload:
            video = self.get_object(video_id)
            video.delete()
            return Response({"detail": "Video Deleted"}, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed("Unauthenticated User")


# USER AUTHENTICATION VIEWS
class RegisterView(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "user registered"}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    '''
        Enables users to login and assigns jwt tokens
    '''

    def post(self, request):
        '''
        Login the user
        '''

        email = request.data["email"]
        password = request.data["password"]

        # Check if user exists
        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("Invalid Credentials")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid Credentials")

        # Create Payload
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # Create and store jwt token in browser cookie
        jwt_token = jwt.encode(payload, settings.JWT_SECRET,
                               algorithm='HS256')
        response = Response()
        response.set_cookie(key='user-token', value=jwt_token, httponly=True)
        response.data = {
            'user-token': jwt_token
        }

        return response


class LogoutView(APIView):
    '''
        This view enables users to logout of their session
    '''

    def get(self, request):
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie("user-token")
        return response

# ################## CATEGORY VIEWS ######################### #


class CategoryListView(generics.ListAPIView):
    '''
        This Api view will list all the video categories
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryView(APIView):

    '''
        This api allows actions to be performed on a single category
    '''

    def is_authenticated(self, request):
        '''
        Authenticate user
        '''
        jwt_token = request.COOKIES.get("user-token")

        payload = authenticate_user(jwt_token)

        try:
            user = User.objects.get(id=payload['id'])
            return user
        except User.DoesNotExist:
            raise Http404

    def post(self, request):
        '''
            Create a new Category
        '''
        if self.is_authenticated(request):
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise AuthenticationFailed("Unauthenticated User")

    def delete(self, request, category_id):
        '''
        Delete Existing Category
        '''
        if self.is_authenticated(request):
            try:
                category = Category.objects.get(id=category_id)
                category.delete()
                return Response({"detail": "Deleted"}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                raise Http404
        else:
            raise AuthenticationFailed("Unauthenticated User")


# #################### LIKE AND DISLIKE API VIEWS ################# #
class LikeView(APIView):
    '''
        This Api view enables authenticated users to like or dislike videos
    '''

    def get_likes(self, video_id):
        try:
            likes = Like.objects.filter(video=video_id)
            return likes
        except Like.DoesNotExist:
            raise Http404

    def liked_user(self, video_id, user_id):
        '''
        Check if user has already liked a video
        '''

        try:
            like = Like.objects.get(user=user_id, video=video_id)
            return False
        except Like.DoesNotExist:
            return True

    def get(self, request, video_id):
        '''
        Get Likes for current video
        '''

        likes = self.get_likes(video_id)
        serializer = LikeSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
        Like a video
        '''
        user = is_authenticated(request)
        if user:
            if self.liked_user(video_id=request.data["video"], user_id=user):
                like_data = {
                    "user": user,
                    "video": request.data["video"],
                    "liked": request.data["liked"]
                }

                serializer = LikeSerializer(data=like_data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed("UnAuthenticated User")

    def put(self, request):
        '''
            Update like object
        '''
        user = is_authenticated(request)
        if user:
            like = Like.objects.get(
                user=user, video=request.data["video"])

            like_data = {
                "user": user,
                "video": request.data["video"],
                "liked": request.data["liked"]
            }
            serializer = LikeSerializer(like, data=like_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            raise AuthenticationFailed("UnAuthenticated User")


class CommentView(APIView):
    '''
        This Api view enables authenticated users to Comment a videos
    '''

    def get_comments(self, video_id):
        try:
            comments = Comment.objects.filter(video=video_id)
            return comments
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, video_id):
        '''
        Get Comments for current video
        '''
        comments = self.get_comments(video_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        '''
        Comment a video
        '''
        user = is_authenticated(request)
        if user:
            comment_data = {
                "user": user,
                "video": request.data["video"],
                "body": request.data["body"]
            }

            serializer = CommentSerializer(data=comment_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            raise AuthenticationFailed("Unauthenticated user")


# ############## PROFILE API VIEW ################ #
class ProfileView(APIView):

    def get_profile(self, user_id):

        try:
            profile = Profile.objects.get(user=user_id)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request):

        user = is_authenticated(request)

        if user:
            profile = self.get_profile(user_id=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
