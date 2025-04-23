from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse


def home(request):
    if request.method == "GET":
        return render(request, 'home/home.html')
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    print(user)
    if user:
        login(request, user)
        return redirect('room', room_name='conversem')

    messages.error(request, "Nome de usuário ou senha inválidos!")
    return render(request, 'home/home.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('avatar')
        bio = request.POST.get('bio')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Esse nome de usuário já existe.")
            return render(request, 'home/register.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Esse email já está cadastrado.")
            return render(request, 'home/register.html')
        else:
            user = User(username=username, email=email, password=make_password(password), image_profile=image, bio=bio)
            user.save()
            messages.success(request, "Você está cadastrado! Faça Login para conversar com alguém.")
            return redirect('home')
    
    return render(request, 'home/register.html')
     

def my_profile(request, username):
    user = get_object_or_404(User, username=username)
    print(user)
    return render(request, 'profiles/profile.html', {'user_profile': user})


def room(request, room_name):
    return render(request, 'chat/chat.html', {'room_name': room_name})