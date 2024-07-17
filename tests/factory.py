import factory

from blog_app.models import Post, Comment, User
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = "xyz"
    password = "user123"
    email = "xyz@gmail.com"


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = "title"
    content = "this is a content"


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    content = "this is a content"
    likes = True

