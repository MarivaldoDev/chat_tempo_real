import datetime
import pytz
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import localtime, now
from django_redis import get_redis_connection


def acesso_negado(request):
    return HttpResponseForbidden(render(request, "home/acesso_negado.html"))


def get_online_key(room_name):
    return f"online_users:{room_name}"


def sao_paulo_now():
    return timezone.now().astimezone(pytz.timezone("America/Sao_Paulo"))


def is_user_online(user_id, room_name):
    conn = get_redis_connection("default")
    return conn.sismember(f"online_users:{room_name}", user_id)


def get_last_seen_display(user_id):
    conn = get_redis_connection("default")
    raw = conn.get(f"user_last_seen:{user_id}")
    if not raw:
        return "Nunca acessou"

    try:
        dt = datetime.datetime.fromisoformat(raw.decode())
    except:
        return "Data inválida"

    tz = pytz.timezone("America/Sao_Paulo")
    local_dt = localtime(dt, timezone=tz)
    now_dt = localtime(now(), timezone=tz)

    hora = local_dt.strftime("%H:%M")

    if local_dt.date() == now_dt.date():
        return f"Visto por último hoje às {hora}"

    dias_semana = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
    dia = dias_semana[local_dt.weekday()]

    return f"Visto por último na {dia} às {hora}"
