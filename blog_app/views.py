from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from blog_app.models import Post, Comment, User
from blog_app.serializers import PostSerializer, CommentSerializer, UserSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions
import logging

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            logger.error("Incorrect input | email: {}".format(email))
            return Response({'detail': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            logger.info("User logged in successfully. | email: {}".format(email))
            return Response({'access': access_token, 'refresh': refresh_token}, status=status.HTTP_200_OK)
        else:
            logger.error("User credentials are incorrect. | email: {}".format(email))
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        logger.info("Creating the Post object.")
        serializer.save(author=self.request.user)


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        post = self.get_object()

        if post.author != self.request.user:
            logger.error("User is not allowed to update the Post | Post: {}".format(post))
            raise PermissionDenied("You do not have permission to edit this post.")
        logger.info("Post object updated successfully | Post: {}".format(post))
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()

        if post.author != request.user:
            logger.error("User is not allowed to delete the Post | Post: {}".format(post))
            raise PermissionDenied("You do not have permission to delete this post.")

        self.perform_destroy(post)
        logger.info("Post object deleted successfully | Post: {}".format(post))
        return Response({"detail": f"Post '{post}' deleted successfully !!!"}, status=status.HTTP_204_NO_CONTENT)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        logger.info("Getting Comment list for the Post | post_id: {}".format(self.kwargs['post_pk']))
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        logger.info("Creating Comment for the Post | post_id: {}".format(self.kwargs['post_pk']))
        post = generics.get_object_or_404(Post, pk=self.kwargs['post_pk'])
        serializer.save(author=self.request.user, post=post)

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        comment = self.get_object()

        if comment.author != self.request.user:
            logger.error("User is not allowed to update the Comment | Comment: {}".format(comment))
            raise PermissionDenied("You do not have permission to edit this post.")
        logger.info("Comment object updated successfully | Comment: {}".format(comment))
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()

        if comment.author != request.user:
            logger.error("User is not allowed to delete the Comment | Comment: {}".format(comment))
            raise PermissionDenied("You do not have permission to delete this post.")

        self.perform_destroy(comment)
        logger.info("Comment object deleted successfully | Comment: {}".format(comment))
        return Response({"detail": f"Comment '{comment}' deleted successfully !!!"}, status=status.HTTP_204_NO_CONTENT)
