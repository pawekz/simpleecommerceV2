from django.shortcuts import render

from accounts.models import Customer
from cart.models import CartItem, Cart


# Create your views here.
def home(request):
    return render(request, 'transaction/payment/payment_basetemplate.html')


def gcash_payment(request):
    context = calculate_cart_subtotal(request)
    return render(request, 'transaction/payment/gcash_payment.html', context)


def maya_payment(request):
    context = calculate_cart_subtotal(request)
    return render(request, 'transaction/payment/maya_payment.html', context)


def cod_payment(request):
    context = calculate_cart_subtotal(request)
    return render(request, 'transaction/payment/cod_payment.html', context)


def credit_payment(request):
    context = calculate_cart_subtotal(request)
    return render(request, 'transaction/payment/credit_payment.html', context)


def success(request):
    return render(request, 'transaction/payment/success.html')


def calculate_cart_subtotal(request):
    # Assuming the user is authenticated and is a customer
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the cart for the current customer
    cart = Cart.objects.get(customer=customer)

    # Fetch all items in the customer's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total_amount for each item in the cart
    subtotal = 0
    for item in cart_items:
        item.total_amount = item.quantity * item.product.PricePerUnit
        subtotal += item.total_amount

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
    }

    return context
