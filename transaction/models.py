from django.db import models
from accounts.models import Customer
from cart.models import Cart
from delivery.models import Delivery
from products.models import Product

# change the default models if necessary
# Create your models here.

class Transaction(models.Model):
    PurchaseDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    TotalPrice = models.DecimalField(max_digits=12, decimal_places=2)
    TotalQuantity = models.IntegerField()
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    Delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True,blank=True)


class OrderHistory(models.Model):
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    TransactionID = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    CartID = models.ForeignKey(Cart, on_delete=models.CASCADE)
    QuantityPerProduct = models.IntegerField()
    DatePurchased = models.DateTimeField(auto_now_add=True, auto_now=False)
    DeliveryID = models.ForeignKey(Delivery, on_delete=models.CASCADE)