from django.db import models


# Create your models here.
class DeliveryType(models.Model):
    DeliveryTypeName = models.CharField(max_length=20)
    DeliveryTypeDescription = models.CharField(max_length=100)
    DeliveryPrice = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.DeliveryTypeName


class Delivery(models.Model):
    DeliveryID = models.IntegerField(primary_key=True)
    DeliveryStatus = models.CharField(max_length=20)
    DeliveryDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    DeliveryType = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.DeliveryID)

