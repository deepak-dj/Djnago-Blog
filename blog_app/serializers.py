from blog_app.models import Post, Comment
from rest_framework import serializers
from blog_app.models import User
import logging

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        logger.info(
            "User has registered | email: {}, username: {}". format(validated_data['email'], validated_data['email'])
        )
        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"detail": "Passwords do not match."})
        return attrs


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, required=False)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'published_date', 'likes_count']

    def get_likes_count(self, obj):
        return obj.count_likes()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Comment
        exclude = ['post']
