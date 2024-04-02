import uuid
import os

from django.db import models
from PIL import Image
from accounts.models import Seller
from datetime import datetime


def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return f'static/product/images/{new_filename}.{ext}'


class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    PricePerUnit = models.DecimalField(max_digits=12, decimal_places=2)
    SellerID = models.ForeignKey(Seller, on_delete=models.CASCADE)
    Quantity = models.IntegerField()
    image = models.ImageField(upload_to=rename_image)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        output_size = (400, 600)
        img.thumbnail(output_size)
        img.save(self.image.path)


class Review(models.Model):
    ReviewID = models.IntegerField(primary_key=True)
    ProductID = models.IntegerField()
    CustomerID = models.IntegerField()
    Rating = models.IntegerField()
    ReviewDate = models.DateTimeField(auto_now_add=True, auto_now=False)