from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from cart.models import Cart, CartItem
from django.shortcuts import get_object_or_404
from accounts.models import Customer
from delivery.models import Delivery, DeliveryType


# Create your views here.
def home(request):
    # add a functionality that chooses the preferred delivery method
    # (see `standard_delivery`, `express_delivery`, `next_day_delivery`)
    # code below

    return render(request, 'delivery/delivery_option.html')


# def standard_delivery(request):
#     # add a functionality that adds the total price of the products in the
#     # cart + the standard delivery fee of 50.00
#     # code below
#
#     return render(request, 'delivery/standard_delivery.html')
#
#
# def express_delivery(request):
#     # add a functionality that adds the total price of the products in the
#     # cart + the express delivery fee of 150.00
#     #code below
#
#     return render(request, 'delivery/express_delivery.html')
#
#
# def next_day_delivery(request):
#     # add a functionality that adds the total price of the products in the
#     # cart + the express delivery fee of 150.00
#     # code below
#
#     return render(request, 'delivery/next_day_delivery.html')


def delivery_option(request):
    if request.method == 'POST':
        selected_delivery_type_id = request.POST.get('delivery_type')
        if selected_delivery_type_id:
            delivery_type = DeliveryType.objects.get(id=selected_delivery_type_id)
            request.session['selected_delivery_type_id'] = selected_delivery_type_id
            request.session['delivery_fee'] = float(delivery_type.DeliveryPrice)  # Convert Decimal to float
            return HttpResponseRedirect(reverse('transaction:review_cart'))  # Redirect to transaction review cart
        else:
            messages.error(request, 'Please select a delivery option.')

    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the cart for the current customer
    cart = get_object_or_404(Cart, customer=customer)

    # Fetch all items in the customer's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Fetch all delivery type options
    delivery_types = DeliveryType.objects.all()

    context = {
        'cart_items': cart_items,
        'delivery_types': delivery_types,
    }

    return render(request, 'delivery/delivery_option.html', context)


def seller_updateorderstatus(request):
    return render(request, 'delivery/seller_updateorderstatus.html')
