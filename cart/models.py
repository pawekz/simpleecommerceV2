from django.db import models


# Create your models here.
class Cart(models.Model):
    CartID = models.IntegerField(primary_key=True)
    ProductID = models.IntegerField()
    QuantityPerProduct = models.IntegerField()
    TransactionID = models.IntegerField()
