from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register_update/<int:id>/', views.register_update, name='register_update'),
    path('chats/', views.chats, name='chats'),
    path('chat/<str:room_name>/', views.room, name='room'),
    path('myprofile/<str:username>/', views.my_profile, name='my_profile'),
    path('logout/', views.logout_view, name='logout'),
    path('acesso_negado/', views.acesso_negado, name='acesso_negado'),
]