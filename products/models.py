from django.db import models

from accounts.models import Seller


# Create your models here.
class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    PricePerUnit = models.DecimalField(max_digits=12, decimal_places=2)
    SellerID = models.ForeignKey(Seller, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/product/images')


class Review(models.Model):
    ReviewID = models.IntegerField(primary_key=True)
    ProductID = models.IntegerField()
    CustomerID = models.IntegerField()
    Rating = models.IntegerField()
    ReviewDate = models.DateTimeField(auto_now_add=True, auto_now=False)
