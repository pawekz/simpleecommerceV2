from django.contrib import admin

#  the purpose of line number "8" is to import the
#  CustomUser, Customer, and Seller models from the models.py file in accounts
#  Specifically in .\accounts\models.py

# Register your models here.
from .models import CustomUser, Customer, Seller

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(Seller)