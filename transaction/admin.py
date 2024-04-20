from django.contrib import admin
from .models import Transaction, OrderHistory, Payment
# Register your models here.

admin.site.register(Transaction)
admin.site.register(OrderHistory)
admin.site.register(Payment)