from django.urls import path
from app.utils import extra_functions
from .views import room_views, user_views, message_views


urlpatterns = [
    path("", user_views.home, name="home"),
    path("register/", user_views.register, name="register"),
    path(
        "register_update/<int:id>/", user_views.register_update, name="register_update"
    ),
    path("lobby/", room_views.lobby, name="chats"),
    path("chats/create_chat", room_views.create_chat, name="create_chat"),
    path("chats/update_chat/<int:id>/", room_views.update_chat, name="update_chat"),
    path("chats/delete_chat/<int:id>/", room_views.delete_chat, name="delete_chat"),
    path("chat/<str:room_name>/", room_views.room, name="room"),
    path("chat/delete_message/<int:id>/", message_views.delete_message, name="delete_message"),
    path("myprofile/<str:username>/", user_views.my_profile, name="my_profile"),
    path(
        "myprofile/deletar/<int:id>/", user_views.delete_profile, name="delete_profile"
    ),
    path("logout/", user_views.logout_view, name="logout"),
    path("acesso_negado/", extra_functions.acesso_negado, name="acesso_negado"),
]
