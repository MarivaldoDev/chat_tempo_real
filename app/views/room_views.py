from app.models import Room, User
from django.shortcuts import render, get_object_or_404, redirect
from app.forms import ChatForm
from django.contrib.auth.decorators import login_required
from django_redis import get_redis_connection
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from app.utils.extra_functions import get_online_key
from django.contrib import messages


@login_required(login_url='home')
def lobby(request):
    rooms = Room.objects.all()
    redis = get_redis_connection("default")

    online_counts = {}
    for room in rooms:
        count = redis.scard(get_online_key(room.name))
        online_counts[room.name] = count
    
    return render(request, 'chat/lobby.html', {'chats': rooms, 'onlines': online_counts})
    
"""     messages.error(request, "Você precisa estar logado para acessar o lobby.")
    return redirect('home') """


@login_required(login_url='home')
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
    
    if form.errors:
        for error in form.errors:
            messages.error(request, form.errors[error])
    
    return render(request, 'chat/create_chat.html', {'form': form})


@login_required(login_url='home')
def update_chat(request, id: int):
    room = get_object_or_404(Room, id=id)
    form = ChatForm(instance=room)

    if request.method == "POST":
        form = ChatForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            return redirect('room', room_name=room.name)
    
    return render(request, 'chat/update_chat.html', {'form': form, 'room': room})


@login_required(login_url='home')
def delete_chat(request, id: int):
    room = get_object_or_404(Room, id=id)

    room.delete()
    messages.success(request, "Sala deletada com sucesso!")
    
    return redirect('chats')


@login_required(login_url='home')
def room(request, room_name: str):
    room = get_object_or_404(Room, name=room_name)
    messages = room.messages.all().order_by('-timestamp')


    return render(request, 'chat/chat.html', {
        'room_name': room_name,
        'room': room, 
        'messages': messages,
    })
