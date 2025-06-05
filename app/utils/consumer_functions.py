from channels.db import database_sync_to_async
from django.utils.timezone import now
from django_redis import get_redis_connection


def get_redis():
    return get_redis_connection("default")


def get_online_key(room_name):
    return f"online_users:{room_name}"


@database_sync_to_async
def add_user_online(room_name, user_id):
    conn = get_redis_connection("default")
    conn.sadd(get_online_key(room_name), user_id)


@database_sync_to_async
def remove_user_online(room_name, user_id):
    conn = get_redis_connection("default")
    conn.srem(get_online_key(room_name), user_id)


@database_sync_to_async
def count_users_online(room_name):
    conn = get_redis_connection("default")
    return conn.scard(get_online_key(room_name))


@database_sync_to_async
def set_last_seen(user_id):
    conn = get_redis_connection("default")
    conn.set(f"user_last_seen:{user_id}", now().isoformat())


def get_global_online_key():
    return "online_users"


@database_sync_to_async
def add_global_user_online(user_id):
    conn = get_redis_connection("default")
    conn.set(f"online_user:{user_id}", 1, ex=60)


@database_sync_to_async
def remove_global_user_online(user_id):
    conn = get_redis_connection("default")
    conn.srem(get_global_online_key(), user_id)


@database_sync_to_async
def is_user_online(user_id):
    conn = get_redis_connection("default")
    result = conn.get(f"online_user:{user_id}")
    print(f"[CHECK ONLINE] user_id={user_id}, is_online={bool(result)}")
    return bool(result)
