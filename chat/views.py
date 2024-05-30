from django.shortcuts import get_object_or_404, redirect, render
from .models import ChatRoom, Message
from accounts.models import Seller, Customer


def create_chat_room(request, seller_id, customer_id):
    # Get the Seller and Customer objects
    seller = get_object_or_404(Seller, pk=seller_id)
    customer = get_object_or_404(Customer, pk=customer_id)

    # Check if a ChatRoom between the given seller and customer already exists
    chat_room = ChatRoom.objects.filter(seller=seller, customer=customer).first()

    # If a ChatRoom does not exist, create a new one
    if chat_room is None:
        chat_room = ChatRoom.objects.create(seller=seller, customer=customer)

    # Redirect to the chat room detail view
    return redirect('chat:view_chat_room', chat_room_id=chat_room.id)


def send_message(request, chat_room_id):
    # Get the ChatRoom object
    chat_room = get_object_or_404(ChatRoom, pk=chat_room_id)

    # Get the message content from the POST data
    content = request.POST.get('content')

    # Check if the user is a seller or a customer
    if hasattr(request.user, 'seller'):
        Message.objects.create(chat_room=chat_room, seller=request.user.seller, content=content)
    elif hasattr(request.user, 'customer'):
        Message.objects.create(chat_room=chat_room, customer=request.user.customer, content=content)

    # Redirect to the chat room detail view
    return redirect('chat:view_chat_room', chat_room_id=chat_room.id)


def view_chat_room(request, chat_room_id):
    # Get the ChatRoom object
    chat_room = get_object_or_404(ChatRoom, pk=chat_room_id)

    # Get all messages in the chat room
    messages = Message.objects.filter(chat_room=chat_room)

    context = {
        'chat_room': chat_room,
        'messages': messages,
    }

    return render(request, 'chat/chat_room.html', context)
