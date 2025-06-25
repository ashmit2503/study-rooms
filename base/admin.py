from django.contrib import admin
from .models import Room, Topic, Message, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin configuration for UserProfile model."""
    list_display = ('user', 'location', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('user__username', 'user__email', 'location')


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin configuration for Topic model."""
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """Admin configuration for Room model."""
    list_display = ('name', 'host', 'topic', 'created')
    list_filter = ('topic', 'created', 'updated')
    search_fields = ('name', 'description', 'host__username')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin configuration for Message model."""
    list_display = ('user', 'room', 'created')
    list_filter = ('room', 'created')
    search_fields = ('body', 'user__username', 'room__name')
