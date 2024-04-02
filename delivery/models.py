from django.db import models


# Create your models here.
class Transaction(models.Model):
    TransactionID = models.IntegerField(primary_key=True)
    PurchaseDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    TotalPrice = models.DecimalField(max_digits=12, decimal_places=2)
    TotalQuantity = models.IntegerField()
    CustomerID = models.IntegerField()
