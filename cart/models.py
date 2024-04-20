from django.contrib.auth.models import User
from django.db import models

from accounts.models import Customer
from products.models import Product

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product)