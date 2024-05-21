from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.models import Customer
from cart.models import CartItem, Cart
from delivery.models import DeliveryType, Delivery
from products.models import Product
from transaction.models import OrderHistory, Transaction
from django.db import transaction


# Create your views here.
def home(request):
    selected_delivery_type_id = request.session.get('selected_delivery_type_id')

    if selected_delivery_type_id is None:
        return redirect('delivery:delivery_option')

    selected_delivery_type = DeliveryType.objects.get(id=selected_delivery_type_id)

    context = {
        'selected_delivery_type': selected_delivery_type,
    }
    return render(request, 'transaction/payment/review_cart.html', context)
    # return render(request, 'transaction/payment/payment_basetemplate.html')


def review_cart(request):
    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the cart for the current customer
    cart = get_object_or_404(Cart, customer=customer)

    # Fetch all items in the customer's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Fetch the selected delivery type
    delivery_type_id = request.session.get('selected_delivery_type_id')
    delivery_type = DeliveryType.objects.get(id=delivery_type_id)

    # Calculate the subtotal (only from the cart)
    subtotal = sum(item.total_amount for item in cart_items)

    # Calculate the total amount
    total_amount = subtotal + delivery_type.DeliveryPrice

    context = {
        'cart_items': cart_items,
        'delivery_type': delivery_type,
        'total_amount': total_amount,
        'subtotal': subtotal,
    }

    return render(request, 'transaction/payment/review_cart.html', context)


def get_payment_context(request):
    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the cart for the current customer
    cart = get_object_or_404(Cart, customer=customer)

    # Fetch all items in the customer's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Fetch the selected delivery type
    delivery_type_id = request.session.get('selected_delivery_type_id')
    delivery_type = DeliveryType.objects.get(id=delivery_type_id)

    # Calculate the subtotal (only from the cart)
    subtotal = sum(item.total_amount for item in cart_items)

    # Calculate the total amount
    total_amount = subtotal + delivery_type.DeliveryPrice

    context = {
        'cart_items': cart_items,
        'delivery_type': delivery_type,
        'total_amount': total_amount,
        'subtotal': subtotal,
    }

    return context


def gcash_payment(request):
    context = get_payment_context(request)
    return render(request, 'transaction/payment/gcash_payment.html', context)


def maya_payment(request):
    context = get_payment_context(request)
    return render(request, 'transaction/payment/maya_payment.html', context)


def cod_payment(request):
    context = get_payment_context(request)
    return render(request, 'transaction/payment/cod_payment.html', context)


def credit_payment(request):
    context = get_payment_context(request)
    return render(request, 'transaction/payment/credit_payment.html', context)


def success(request):
    messages.success(request, 'Your payment was successful!')
    return render(request, 'transaction/payment/success.html')


@login_required
def confirm_payment(request):
    print("confirm_payment called")
    try:
        with transaction.atomic():
            cart = get_cart(request)
            print("Cart retrieved: ", cart)
            if transaction_exists(cart) or cart_is_empty(cart):
                print("transaction already exists or cart is empty")
                return redirect('transaction:success')

            cart_items = lock_cart_items(cart)
            print("Cart items locked:", cart_items)

            new_transaction = save_new_transaction(request, cart, cart_items)
            print("New transaction saved:", new_transaction)

            delivery = save_new_delivery(request)
            print("Delivery saved:", delivery)

            process_cart_items(cart_items, new_transaction, cart, delivery)
            print("Cart items processed")

    except Exception as e:
        print("Exception ocured: ", e)
        return redirect('transaction:error')

    print("Payment confirmed successfully")
    return redirect('transaction:success')


def get_cart(request):
    print("Fetching cart for the user called get_cart")
    return Cart.objects.get(customer=request.user.customer)


def transaction_exists(cart):
    print("Checking if transaction already exists called transaction_exist")
    return Transaction.objects.filter(Cart=cart).exists()


def cart_is_empty(cart):
    print("Checking if cart is empty called cart_is_empty")
    return not cart.cartitem_set.exists()


def lock_cart_items(cart):
    print("Locking cart items called lock_cart_items")
    return CartItem.objects.select_for_update().filter(cart=cart)


def save_new_transaction(request, cart, cart_items):
    print("Creating a new transaction called save_new_transaction")
    new_transaction = Transaction(
        PurchaseDate=timezone.now(),
        TotalPrice=cart.total,
        TotalQuantity=cart_items.count(),
        CustomerID=request.user.customer,
        Cart=cart
    )
    new_transaction.save()
    return new_transaction


def save_new_delivery(request):
    print("Saving a new delivery called save_new_delivery")
    selected_delivery_type_id = request.session.get('selected_delivery_type_id')
    delivery_type = DeliveryType.objects.get(id=selected_delivery_type_id)
    # dnhi na ka mag modify pre sa `DeliveryStatus`
    delivery = Delivery(DeliveryStatus='1', DeliveryType=delivery_type)
    delivery.save()
    return delivery


def process_cart_items(cart_items, new_transaction, cart, delivery):
    print("Processing cart items called process_cart_items")
    for item in cart_items:
        if item.product is None:
            continue
        print("Saving order history for item:", item)
        order_history = save_order_history(item, new_transaction, cart, delivery)
        if product_quantity_insufficient(item):
            return redirect('transaction:error')
        update_product_quantity(item)
        delete_cart_item(item)


def save_order_history(item, new_transaction, cart, delivery):
    print("Creating order history called save_order_history: ", item)
    order_history = OrderHistory(
        ProductID=item.product,
        TransactionID=new_transaction,
        CartID=cart,
        QuantityPerProduct=item.quantity,
        DatePurchased=timezone.now(),
        DeliveryID=delivery
    )
    order_history.save()
    return order_history


def product_quantity_insufficient(item):
    print("Check product quantity for item called product_quantity_insufficient:", item)
    return item.product.Quantity < item.quantity


def update_product_quantity(item):
    print("Updating product quantity for item called update_product_quantity:", item)
    item.product.Quantity -= item.quantity
    item.product.save()


def delete_cart_item(item):
    print("Deleting cart item:", item)
    item.delete()


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


def payment_option(request):
    return render(request, 'transaction/payment/payment_basetemplate.html')


def error(request):
    return render(request, 'transaction/error.html')
