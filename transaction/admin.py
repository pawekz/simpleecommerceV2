from django.contrib import admin
from .models import OrderHistory, Payment, Transaction
# Register your models here.

admin.site.register(OrderHistory)
admin.site.register(Payment)
admin.site.register(Transaction)

