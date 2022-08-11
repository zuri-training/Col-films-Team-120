from rest_framework import serializers
from video.models import Category, Comment, Like, Profile, Video
from members.models import Member
from rest_framework import status


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title",)


class VideoSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    video_file = serializers.SerializerMethodField('get_video')
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # comments =
    # likes = serializers.StringRelatedField(read_only=True)

    def get_video(self, instance):
        return "http://127.0.0.1:8000/media/{}".format(instance.video_file)

    class Meta:
        model = Video
        fields = "__all__"

    def create(self, validated_data):
        published = validated_data.pop("published")

        instance = self.Meta.model(**validated_data)
        instance.published = bool(int(published))


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("first_name", "last_name",
                  "school", "email", "password")

    def validate_email(self, email):
        """
        Check the email to ensure a valid student email is passed
        """
        if ".edu" not in email.split("@")[1]:
            raise serializers.ValidationError(
                "Email must be a school email", code=status.HTTP_400_BAD_REQUEST)
        return email

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

        # def create(self, validated_data):
        #     liked = validated_data.pop("liked")
        #     instance = self.Meta.model(**validated_data)
        #     instance.liked = bool(int(liked))


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
