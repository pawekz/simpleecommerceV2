from django.contrib.auth.models import User
from django.db import models
from accounts.models import Customer
from products.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_amount = models.DecimalField(decimal_places=2, max_digits=12, null=True)
