"""
URL patterns for the base StudyRooms application.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_page, name="login"), 
    path("home/", views.home, name="home"), 
    
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("logout/", views.logout_user, name="logout"),
    
    path("profile/edit/", views.edit_profile, name="edit-profile"),
    path("profile/delete/", views.delete_profile, name="delete-profile"),
    path("profile/<str:username>/", views.user_profile, name="user-profile"),
    
    path("room/<str:pk>/", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),
    path("update-room/<str:pk>/", views.update_room, name="update-room"),
    path("delete-room/<str:pk>/", views.delete_room, name="delete-room"),
    path("delete-message/<str:pk>", views.delete_message, name="delete-message"),
    
    path("api/room/<str:pk>/messages/", views.get_room_messages, name="get-room-messages"),
]
