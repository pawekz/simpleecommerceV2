from django.db import models
from django.contrib.auth.models import User
from accounts.models import Customer, Seller


class ChatRoom(models.Model):
    # Auto incrementing unique id for each chat room
    id = models.AutoField(primary_key=True)
    # Foreign key to the Seller model for the seller
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='seller_chat_rooms')
    # Foreign key to the Customer model for the customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_chat_rooms')


class Message(models.Model):
    # Foreign key to the ChatRoom model
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    # Foreign key to the Seller model for the seller
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    # Foreign key to the Customer model for the customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    # Text field for the message content
    content = models.TextField()
    # Timestamp for when the message was sent
    timestamp = models.DateTimeField(auto_now_add=True)
