from django.contrib import admin
from .models import Delivery, DeliveryType
# Register your models here.

admin.site.register(Delivery)
admin.site.register(DeliveryType)


