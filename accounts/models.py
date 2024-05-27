from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import BaseUserManager, Group, Permission, PermissionsMixin, User
from django.conf import settings



class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


#  it is necessary to implement this CustomUser class to avoid clashes with the built-in User model.
#  This is because the built-in User model is not a custom model, and it is not recommended to modify it.
#  Instead, it is recommended to create a new model that inherits from the built-in User model.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=64)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    @property
    def is_customer(self):
        return hasattr(self, 'customer')

    @property
    def is_seller(self):
        return hasattr(self, 'seller')


class Customer(CustomUser):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    contact_no = models.CharField(max_length=11)
    address = models.CharField(max_length=255)


class Seller(CustomUser):
    seller_id = models.AutoField(primary_key=True)
    seller_name = models.CharField(max_length=255)
    stall_name = models.CharField(max_length=64)
    contact_no = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
