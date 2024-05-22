
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View

from chat.models import ChatRoom,Message


class MessageCreateView(View):
    def post(self, request, chat_room_id):
        chat_room = ChatRoom.objects.get(id=chat_room_id)
        user = request.user
        content = request.POST.get('content')
        Message.objects.create(chat_room=chat_room, user=user, content=content)
        return HttpResponseRedirect(reverse('chat:chat_room_detail', args=[chat_room_id]))