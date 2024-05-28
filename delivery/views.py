from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from cart.models import Cart, CartItem
from django.shortcuts import get_object_or_404
from accounts.models import Customer
from delivery.models import Delivery, DeliveryType
from transaction.models import Transaction


# Create your views here.
def home(request):
    # add a functionality that chooses the preferred delivery method
    # (see `standard_delivery`, `express_delivery`, `next_day_delivery`)
    # code below

    return render(request, 'delivery/delivery_option.html')


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
    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        cart = Cart.objects.create(customer=customer, total=0.00)

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
    return render(request, 'transaction/seller_update_order_status.html')


def cust_trackdelivery(request, transaction_id=None):
    if transaction_id is not None:
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        return render(request, 'transaction/customer_trackdelivery.html',
                      {'status': transaction.status})
    transaction = get_object_or_404(Transaction, pk=transaction_id)  # Fetch Transaction instead of Order
    return render(request, 'transaction/customer_trackdelivery.html',
                  {'status': transaction.status})  # Use transaction.status instead of order.status


def customer_trackdelivery(request):
    return render(request, 'transaction/customer_trackdelivery.html')
