from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts.models import Customer
from cart.models import CartItem, Cart
from delivery.models import DeliveryType, Delivery
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


def confirm_payment(request):
    # Get the current user's cart
    cart = Cart.objects.get(customer=request.user.customer)

    try:
        with transaction.atomic():
            # Create a new Transaction instance
            new_transaction = Transaction(
                PurchaseDate=timezone.now(),
                TotalPrice=cart.total,
                TotalQuantity=cart.cartitem_set.count(),  # Assumes each CartItem represents one product
                CustomerID=request.user.customer  # Assign the Customer instance directly
            )
            new_transaction.save()

            # Get the first Delivery object, or create a new one if none exist
            delivery = Delivery.objects.first()
            if delivery is None:
                delivery_type = DeliveryType.objects.first()  # Assumes a DeliveryType exists
                delivery = Delivery(DeliveryStatus='To Pack', DeliveryType=delivery_type)
                delivery.save()  # Save the Delivery instance to the database

            # Create a new OrderHistory instance for each item in the cart
            for item in cart.cartitem_set.all():
                if item.product is None:
                    print(f"CartItem with id {item.id} does not have an associated product.")
                    continue
                order_history = OrderHistory(
                    ProductID=item.product,  # Assign the Product instance directly
                    TransactionID=new_transaction,
                    CartID=cart,
                    QuantityPerProduct=item.quantity,  # Use QuantityPerProduct instead of Quantity
                    DatePurchased=timezone.now(),
                    DeliveryID=delivery  # Use the Delivery object
                )
                order_history.save()

                item.product.Quantity -= item.quantity
                item.product.save()

    except Exception as e:
        # Handle the exception
        print(f"An error occurred: {e}")
        return redirect('transaction:error')  # Redirect to an error page

    # Redirect to the success page
    return redirect('transaction:success')


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
