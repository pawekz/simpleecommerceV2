from django.db import models


# change the default models if necessary
# Create your models here.
class OrderHistory(models.Model):
    OrderID = models.IntegerField(primary_key=True)
    ProductID = models.IntegerField()
    TransactionID = models.IntegerField()
    CartID = models.IntegerField()
    PaymentID = models.IntegerField()
    QuantityPerProduct = models.IntegerField()
    DatePurchased = models.DateTimeField(auto_now_add=True, auto_now=False)
    DeliveryID = models.IntegerField()


class Payment(models.Model):
    PaymentID = models.IntegerField(primary_key=True)
    PaymentDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    PaymentMethod = models.CharField(max_length=20)


class Transaction(models.Model):
    TransactionID = models.IntegerField(primary_key=True)
    PurchaseDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    TotalPrice = models.DecimalField(max_digits=12, decimal_places=2)
    TotalQuantity = models.IntegerField()
    CustomerID = models.IntegerField()
