from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from accounts.models import Customer, CustomUser
from cart.models import CartItem, Cart
from delivery.models import DeliveryType, Delivery
from products.models import Product
from .models import OrderHistory, Transaction
from django.db import transaction
from .models import OrderHistory, Transaction
from .forms import UpdateOrderStatusForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


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
    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        cart = Cart.objects.create(customer=customer, total=0.00)

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
    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        cart = Cart.objects.create(customer=customer, total=0.00)

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
    print("starting confirm_payment")

    if 'payment_confirmed' in request.session:
        print("payment already confirmed going back to main menu")
        del request.session['payment_confirmed']  # Clear the 'payment_confirmed' session variable
        return redirect('accounts:main_menu')

    customer = Customer.objects.get(customuser_ptr=request.user)
    print(f"call customer ID: {customer}")

    try:
        with transaction.atomic():
            # Get the current user's cart
            cart = Cart.objects.filter(customer=customer).order_by('-id').first()
            if cart is None:
                cart = Cart.objects.create(customer=customer, total=0.00)
            print(f"Cart: {cart}")

            # Lock the cart items until the transaction is complete
            cart_items = CartItem.objects.select_for_update().filter(cart=cart)
            print(f"Cart items: {cart_items}")

            # Get the preferred DeliveryType from the session
            delivery_type_id = request.session.get('selected_delivery_type_id')
            delivery_type = DeliveryType.objects.get(id=delivery_type_id)

            # Always create a new Delivery instance
            delivery = Delivery(DeliveryType=delivery_type)
            delivery.save()  # Save the Delivery instance to the database
            print(f"Delivery : {delivery}")
            print("Delivery Save")

            # First loop: Validate cart items
            for item in cart_items:
                if item.product is None:
                    continue

                # Check if the product quantity is less than the quantity in the cart
                if item.product.Quantity < item.quantity:
                    logger.warning(f"Product {item.product.ProductID} is out of stock")
                    return redirect('transaction:error')  # Redirect to an error page

            # Create a new Transaction instance
            new_transaction = Transaction(
                PurchaseDate=timezone.now(),
                TotalPrice=cart.total,
                TotalQuantity=cart_items.count(),  # Assumes each CartItem represents one product
                CustomerID=request.user.customer,  # Assign the Customer instance directly
                Cart=cart,  # Assign the Cart instance
                Delivery=delivery  # Assign the Delivery instance
            )
            print("Transaction about to save")
            new_transaction.save()

            # Second loop: Process cart items
            for item in cart_items:
                if item.product is None:
                    continue

                order_history = OrderHistory(
                    ProductID=item.product,  # Assign the Product instance directly
                    TransactionID=new_transaction,
                    CartID=cart,
                    QuantityPerProduct=item.quantity,  # Use QuantityPerProduct instead of Quantity
                    DatePurchased=timezone.now(),
                    DeliveryID=delivery  # Use the Delivery object
                )
                print("Order History about to save")
                order_history.save()

                # Update product quantity
                # item.product.Quantity -= item.quantity
                item.product.save()
                logger.info(f"Product {item.product.ProductID} quantity updated")
                print(f"Product {item.product.ProductID} quantity updated")

                # Delete the CartItem instance after updating product quantity
                item.delete(update_product_quantity=False)
                logger.info(f"Cart items for cart {cart.id} deleted")
                print(f"Cart items for cart {cart.id} deleted")

            # Create a new Cart instance for the customer
            print("About to create new instance of the cart")
            new_cart = Cart(customer=request.user.customer, total=0.00)
            new_cart.save()

            request.session['cart_id'] = new_cart.id

            if 'cart_id' in request.session:
                del request.session['cart_id']
            if 'payment_confirmed' in request.session:
                del request.session['payment_confirmed']

    except Exception as e:
        # Handle the exception
        logger.error(f"An error occurred: {e}")
        return redirect('transaction:error')  # Redirect to an error page

    request.session['payment_confirmed'] = True
    # Redirect to the success page
    return redirect('transaction:payment_successful', transaction_id=new_transaction.id)

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


def order_history(request):
    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the Cart instances for the current customer
    carts = Cart.objects.filter(customer=customer)

    # Fetch the OrderHistory instances for the current customer
    order_history = OrderHistory.objects.filter(CartID__in=carts)

    context = {
        'order_history': order_history,
    }

    return render(request, 'transaction/customer_order_history.html', context)


# def payment_successful(request):
#     return render(request, 'transaction/payment/payment_successful.html')
# In transaction/views.py
def payment_successful(request, transaction_id):
    if 'payment_confirmed' in request.session:
        del request.session['payment_confirmed']
    return render(request, 'transaction/payment/payment_successful.html', {'transaction_id': transaction_id})


def customer_trackdelivery(request, transaction_id):  # Use transaction_id instead of order_id
    transactions = get_object_or_404(Transaction, pk=transaction_id)  # Fetch Transaction instead of Order
    return render(request, 'transaction/customer_trackdelivery.html',
                  {'status': transactions.status})  # Use transaction.status instead of order.status


def customer_order_history(request, customer_id):
    order_histories = OrderHistory.objects.filter(CustomerID=customer_id)
    order_statuses = [get_object_or_404(Transaction, pk=order_history.TransactionID.pk).status for order_history in
                      order_histories]
    total_prices = [get_object_or_404(Transaction, pk=order_history.TransactionID.pk).TotalPrice for order_history in
                    order_histories]
    return render(request, 'transaction/customer_order_history.html',
                  {'order_histories': order_histories, 'order_statuses': order_statuses, 'total_prices': total_prices})


def seller_order_history(request):
    # Get all OrderHistory instances
    order_history = OrderHistory.objects.all()

    context = {
        'order_history': order_history,
    }

    return render(request, 'transaction/seller_order_history.html', context)


@csrf_exempt
def ajax_update_order_status(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        transaction = get_object_or_404(Transaction, pk=order_id)
        transaction.status = new_status
        transaction.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
