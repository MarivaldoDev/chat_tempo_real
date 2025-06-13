import cowsay
from asgiref.sync import async_to_sync
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from app.consumers import is_user_online
from app.forms import LoginForm, UserForm
from app.models import User
from app.utils.extra_functions import get_last_seen_display


def home(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "home/home.html", {"form": form})

    form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            """ cowsay.python(f"Usuário {username} fez login!") """

            return redirect("chats")
    else:
        for error in form.errors:
            messages.error(request, form.errors[error])
    return render(request, "home/home.html", {"form": form})


def register(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "home/register.html", {"form": form})

    form = UserForm(request.POST, request.FILES)

    if form.is_valid():
        user = form.save(commit=False)
        user.password = make_password(form.cleaned_data["password"])
        user.save()
        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect("home")

    if form.errors:
        for error in form.errors:
            messages.error(request, form.errors[error])

    return render(request, "home/register.html", {"form": form})


@login_required(login_url="acesso_negado")
def register_update(request, id: int):
    user = get_object_or_404(User, id=id)
    form = UserForm(instance=user)

    if user != request.user:
        return redirect("acesso_negado")
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password"])
            user.save()
            update_session_auth_hash(request, user)
            print("ok")
            return redirect("my_profile", username=request.user.username)

        if form.errors:
            for error in form.errors:
                messages.error(request, form.errors[error])

    return render(request, "home/register_update.html", {"form": form, "user": user})


@login_required(login_url="acesso_negado")
def my_profile(request, username: str):
    user = get_object_or_404(User, username=username)
    online_status = bool(async_to_sync(is_user_online)(user.id))

    if online_status:
        status = "Online"
    else:
        status = get_last_seen_display(user.id)
    return render(
        request,
        "profiles/profile.html",
        {"user": user, "request_user": request.user, "status": status},
    )


@login_required(login_url="acesso_negado")
def delete_profile(request, id: int):
    user = get_object_or_404(User, id=id)

    user.delete()
    messages.success(request, "Usuário deletado com sucesso!")

    return redirect("home")


@login_required(login_url="home")
def logout_view(request):
    logout(request)
    return redirect("home")


def acesso_negado(request):
    return HttpResponseForbidden(render(request, "home/acesso_negado.html"))


def not_found(request, exception):
    return render(request, "errors/404.html", status=404)