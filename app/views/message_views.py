from app.models import Message
from django.shortcuts import get_object_or_404, redirect


def delete_message(request, id: int):
    message = get_object_or_404(Message, id=id)

    message.delete()
    return redirect('room', message.room)