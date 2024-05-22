from django.db import models
from accounts.models import Customer
from cart.models import Cart
from delivery.models import Delivery
from products.models import Product

# change the default models if necessary
# Create your models here.

class Transaction(models.Model):
    PurchaseDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    TotalPrice = models.DecimalField(max_digits=12, decimal_places=2)
    TotalQuantity = models.IntegerField()
    CustomerID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_quantity = models.IntegerField()

    PACKED = 'Packed and Ready to Ship'
    PICKED_UP = 'Package Picked Up'
    ARRIVED = 'Arrived at Sort Center'
    DEPARTED = 'Departed from Sort Center'
    ABOUT_TO_DELIVER = 'About to Deliver'
    DELIVERED = 'Delivered'

    SHIPMENT_STATUS_CHOICES = [
        (PACKED, 'Packed and Ready to Ship'),
        (PICKED_UP, 'Package Picked Up'),
        (ARRIVED, 'Arrived at Sort Center'),
        (DEPARTED, 'Departed from Sort Center'),
        (ABOUT_TO_DELIVER, 'About to Deliver'),
        (DELIVERED, 'Delivered'),
    ]

    shipment_status = models.CharField(
        max_length=30,
        choices=SHIPMENT_STATUS_CHOICES,
        default=PACKED,
    )

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.ProductName}"


class OrderHistory(models.Model):
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    TransactionID = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    CartID = models.ForeignKey(Cart, on_delete=models.CASCADE)
    QuantityPerProduct = models.IntegerField()
    DatePurchased = models.DateTimeField(auto_now_add=True, auto_now=False)
    DeliveryID = models.ForeignKey(Delivery, on_delete=models.CASCADE)