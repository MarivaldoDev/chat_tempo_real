from django.shortcuts import render, redirect
from .models import User
from django.http import HttpResponse


def home(request):
    return render(request, 'home/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('avatar')
        bio = request.POST.get('bio')

        if User.objects.filter(username=username).exists():
            return HttpResponse("Esse nome de usuário já existe.")
        elif User.objects.filter(email=email).exists():
            return HttpResponse("Esse email já está cadastrado.")
        else:
            user = User(username=username, email=email, password=password, image_profile=image, bio=bio)
            user.save()
            return render(request, 'home/register.html', {"success_message": "Usuário cadastrado com sucesso!"})
    
    return render(request, 'home/register.html')
     

def room(request, room_name):
    return render(request, 'chat/chat.html', {'room_name': room_name})