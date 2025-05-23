from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Room
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm, LoginForm, ChatForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseForbidden
from django_redis import get_redis_connection
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import cowsay


def get_online_key(room_name):
    return f"online_users:{room_name}"


def home(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'home/home.html', {'form': form})
    
    form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            cowsay.python(f'Usuário {username} fez login!')
            return redirect('chats')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error])
    return render(request, 'home/home.html', {'form': form})


def register(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'home/register.html', {'form': form})
    
    form = UserForm(request.POST, request.FILES)

    if form.is_valid():
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data['password'])
        user.save()
        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect('home')
    
    if form.errors:
        for error in form.errors:
            messages.error(request, form.errors[error])
    return render(request, 'home/register.html', {'form': form})


@login_required(login_url='acesso_negado')
def register_update(request, id: int):
    user = get_object_or_404(User, id=id)
    form = UserForm(instance=user)
    
    if user != request.user:
        return redirect('acesso_negado')
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            update_session_auth_hash(request, user)
            print('ok')
            return redirect('my_profile', username=request.user.username)

        if form.errors:
            for error in form.errors:
                messages.error(request, form.errors[error])
             
    return render(request, 'home/register_update.html', {'form': form, 'user': user})
     

@login_required(login_url='acesso_negado')
def my_profile(request, username: str):
    user = get_object_or_404(User, username=username)
    return render(request, 'profiles/profile.html', {'user': user, 'request_user': request.user})


def delete_profile(request, id: int):
    user = get_object_or_404(User, id=id)

    user.delete()
    messages.success(request, "Usuário deletado com sucesso!")
    
    return redirect('home')


@login_required(login_url='home')
def logout_view(request):
    logout(request)
    return redirect('home')


def lobby(request):
    rooms = Room.objects.all()
    redis = get_redis_connection("default")

    online_counts = {}
    for room in rooms:
        count = redis.scard(get_online_key(room.name))
        online_counts[room.name] = count
    
    return render(request, 'chat/lobby.html', {"chats": rooms, 'onlines': online_counts})


def create_chat(request):
    form = ChatForm()
    if request.method == 'GET':
        return render(request, 'chat/create_chat.html', {'form': form})
    
    form = ChatForm(request.POST)
    if form.is_valid():
        room = form.save(commit=False)
        room.save()
        room.users.add(request.user)
        messages.success(request, "Sala criada com sucesso!")

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        "lobby",
        {
            "type": "new_room",
            "room": {
                "name": room.name,
                "description": room.description,
            }
        }
    )
        return redirect('room', room_name=room.name)
    
    return render(request, 'chat/create_chat.html', {'form': form})


@login_required(login_url='home')
def room(request, room_name: str):
    room = get_object_or_404(Room, name=room_name)
    messages = room.messages.all().order_by('-timestamp')


    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'room': room, 
        'messages': messages,
    })


def acesso_negado(request):
    return HttpResponseForbidden(render(request, 'home/acesso_negado.html'))