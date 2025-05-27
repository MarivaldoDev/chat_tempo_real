from django.http import HttpResponseForbidden
from django.shortcuts import render


def acesso_negado(request):
    return HttpResponseForbidden(render(request, 'home/acesso_negado.html'))


def get_online_key(room_name):
    return f"online_users:{room_name}"
