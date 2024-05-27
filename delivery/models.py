from django.db import models


# Create your models here.
class DeliveryType(models.Model):
    DeliveryTypeName = models.CharField(max_length=20)
    DeliveryTypeDescription = models.CharField(max_length=100)
    DeliveryPrice = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.DeliveryTypeName


class Delivery(models.Model):
    DeliveryID = models.AutoField(primary_key=True)
    DeliveryDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    DeliveryType = models.ForeignKey(DeliveryType, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.DeliveryID)



class DeliveryStatus(models.Model):
    STATUS_CHOICES = [
        ('PR', 'Packed and Ready to Ship'),
        ('PU', 'Package Picked Up'),
        ('AS', 'Arrived at Sort Center'),
        ('DS', 'Departed from Sort Center'),
        ('AD', 'About to Deliver'),
        ('DE', 'Delivered'),
    ]

    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='delivery_statuses')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PR')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.delivery.id} - {self.get_status_display()}'