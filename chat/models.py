from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    # Auto incrementing unique id for each chat room
    id = models.AutoField(primary_key=True)

class Message(models.Model):
    # Foreign key to the ChatRoom model
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    # Foreign key to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Text field for the message content
    content = models.TextField()
    # Timestamp for when the message was sent
    timestamp = models.DateTimeField(auto_now_add=True)