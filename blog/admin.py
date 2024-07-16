from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import (
    User, 
    Post, 
    Commentary
    )


admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_time')
    search_fields = ('title', 'content', 'owner__username', 'owner__email')
    list_filter = ('created_time', 'owner')

@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_time', 'content')
    search_fields = ('content', 'user__username', 'user__email', 'post__title')
    list_filter = ('created_time', 'user', 'post')