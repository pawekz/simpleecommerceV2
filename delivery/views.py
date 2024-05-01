from django.shortcuts import render, redirect
from cart.models import Cart, CartItem
from django.shortcuts import get_object_or_404
from accounts.models import Customer
from delivery.models import Delivery

# Create your views here.
def home(request):
    # add a functionality that chooses the preferred delivery method
    # (see `standard_delivery`, `express_delivery`, `next_day_delivery`)
    # code below

    return render(request, 'delivery/delivery_option.html')


def standard_delivery(request):
    # add a functionality that adds the total price of the products in the
    # cart + the standard delivery fee of 50.00
    # code below

    return render(request, 'delivery/standard_delivery.html')


def express_delivery(request):
    # add a functionality that adds the total price of the products in the
    # cart + the express delivery fee of 150.00
    #code below

    return render(request, 'delivery/express_delivery.html')


def next_day_delivery(request):
    # add a functionality that adds the total price of the products in the
    # cart + the express delivery fee of 150.00
    # code below

    return render(request, 'delivery/next_day_delivery.html')


def delivery_option(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the cart for the current customer
    cart = get_object_or_404(Cart, customer=customer)

    # Fetch all items in the customer's cart
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'delivery/delivery_option.html', context)


def seller_updateorderstatus(request):
    return render(request, 'delivery/seller_updateorderstatus.html')