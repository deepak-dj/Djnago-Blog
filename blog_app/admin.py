from django.contrib import admin
from .models import Post, Comment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', 'is_staff')
    search_fields = ('email', 'username')
    list_filter = ('is_active', 'is_staff')
    ordering = ('email',)
    readonly_fields = ('last_login',)  # Include if you have last_login field


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content')
    list_filter = ('author', 'published_date')
    ordering = ('-published_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'likes')
    search_fields = ('content',)
    list_filter = ('post', 'author', 'likes')
    ordering = ('-created_at',)
