from django.contrib import admin
from .models import Transaction, OrderHistory
# Register your models here.

admin.site.register(Transaction)
admin.site.register(OrderHistory)
