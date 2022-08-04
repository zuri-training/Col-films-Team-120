from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import jwt
import datetime
from django.conf import settings

# Custom imports
from .serializers import CategorySerializer, VideoSerializer
from video.models import Category, Video
from .functions import authenticate_user


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
        video = self.get_object()
        serializer = VideoSerializer(data=video)
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
            "categories": [int(request.data["categories"]), ]
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
                "categories": [int(request.data["categories"])],
                "published": bool(request.data["published"]),
            }

            serializer = VideoSerializer(video, data=video_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"detail": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


class VideoDeleteView(generics.DestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


# USER AUTHENTICATION VIEWS
class LoginView(APIView):
    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("Invalid Credentials")

        if not user.check_password(password):
            raise AuthenticationFailed("Invalid Credentials")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        jwt_token = jwt.encode(payload, settings.JWT_SECRET,
                               algorithm='HS256')
        response = Response()
        response.set_cookie(key='user-token', value=jwt_token, httponly=True)
        response.data = {
            'user-token': jwt_token
        }

        return response


# ################## CATEGORY VIEWS ######################### #
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryView(APIView):

    def is_authenticated(self, request):

        jwt_token = request.COOKIES.get("user-token")

        payload = authenticate_user(jwt_token)

        try:
            user = User.objects.get(id=payload['id'])
            return user
        except User.DoesNotExist:
            raise Http404

    def post(self, request):
        if self.is_authenticated(request):
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"detail": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise AuthenticationFailed("Unauthenticated User")

    def delete(self, request, category_id):
        if self.is_authenticated(request):
            try:
                category = Category.objects.get(id=category_id)
                category.delete()
                return Response({"detail": "Deleted"}, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                raise Http404
        else:
            raise AuthenticationFailed("Unauthenticated User")
