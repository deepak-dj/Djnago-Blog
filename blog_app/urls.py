from rest_framework import permissions
from django.contrib import admin
from blog_app.views import PostListCreateAPIView, PostDetailAPIView, CommentListCreateAPIView, CommentDetailAPIView
from django.urls import path, include, re_path
from blog_app import views
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="""
                <h2> Base URL: <strong>127.0.0.1:8000/api</strong> </h2>
                <p><strong>This is the base URL for all API endpoints. Use this base URL when making API requests.</strong></p>
                """,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('register', views.UserViewSet, basename='register')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('api/posts/<int:post_pk>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('api/posts/<int:post_pk>/comments/<int:pk>/', CommentDetailAPIView.as_view(), name='comment-list-detail'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
