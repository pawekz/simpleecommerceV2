from django.urls import path, include
from . import views

app_name = 'chat'

urlpatterns = [
    # URL pattern for creating a new chat room
    path('chatroom/create/<int:seller_id>/<int:customer_id>/', views.create_chat_room, name='create_chat_room'),
    # URL pattern for sending a message
    path('message/send/<int:chat_room_id>/', views.send_message, name='send_message'),
    # URL pattern for viewing a chat room
    path('chatroom/<int:chat_room_id>/', views.view_chat_room, name='view_chat_room'),

    #path('chat/', include(('chat.urls', 'chat'), namespace='chat')),
]