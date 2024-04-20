from django.db import models


# Create your models here.
class Delivery(models.Model):
    DeliveryID = models.IntegerField(primary_key=True)
    DeliveryStatus = models.CharField(max_length=20)
    DeliveryDate = models.DateTimeField(auto_now_add=True, auto_now=False)
