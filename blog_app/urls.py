from blog_app.views import PostListCreateAPIView, PostDetailAPIView, CommentListCreateAPIView, CommentDetailAPIView
from django.urls import path, include
from blog_app import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('register', views.UserViewSet, basename='register')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginView.as_view(), name='login'),
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/<int:post_pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('posts/<int:post_pk>/comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-list-detail'),
]
