from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserForm, LoginForm
from django.contrib.auth.decorators import login_required


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
            return redirect('room', room_name='testes')
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
     

@login_required(login_url='home')
def my_profile(request, username):
    user = get_object_or_404(User, username=username)
    print(user)
    return render(request, 'profiles/profile.html', {'user_profile': user})


@login_required(login_url='home')
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='home')
def room(request, room_name):
    return render(request, 'chat/chat.html', {'room_name': room_name})