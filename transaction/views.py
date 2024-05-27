from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from accounts.models import Customer
from cart.models import CartItem, Cart
from delivery.models import DeliveryType, Delivery
from products.models import Product, ProductReview
from transaction.models import OrderHistory, Transaction
from django.db import transaction

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

            # Check if a transaction has already been created for this cart
            if Transaction.objects.filter(Cart=cart).exists():
                logger.info(f"Transaction already exists for cart {cart.id}")
                print(f"Transaction already exists for cart {cart.id}")
                return redirect('transaction:payment_successful')  # Redirect to the success page

            # Check if the cart is already empty
            if not cart.cartitem_set.exists():
                logger.info('Cart is empty')
                print("Cart is empty")
                return redirect('transaction:payment_successful')  # Redirect to the success page

            # Lock the cart items until the transaction is complete
            cart_items = CartItem.objects.select_for_update().filter(cart=cart)
            print(f"Cart items: {cart_items}")

            # Get the preferred DeliveryType from the session
            delivery_type_id = request.session.get('selected_delivery_type_id')
            delivery_type = DeliveryType.objects.get(id=delivery_type_id)

            # Get the first Delivery object for the preferred DeliveryType, or create a new one if none exist
            delivery = Delivery.objects.filter(DeliveryType=delivery_type).first()
            if delivery is None:
                delivery = Delivery(DeliveryStatus='1', DeliveryType=delivery_type)
                delivery.save()  # Save the Delivery instance to the database
            print(f"Delivery : {delivery}")
            print("Delivery Save")


            # Create a new Transaction instance
            new_transaction = Transaction(
                PurchaseDate=timezone.now(),
                TotalPrice=cart.total,
                TotalQuantity=cart_items.count(),  # Assumes each CartItem represents one product
                CustomerID=request.user.customer,  # Assign the Customer instance directly
                Cart=cart,  # Assign the Cart instance
                Delivery=delivery #Assign the Delivery instance
            )
            print("Transaction about to save")
            new_transaction.save()

            cart.delivery = delivery
            cart.save()

            # Create a new OrderHistory instance for each item in the cart
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

                # Check if the product quantity is less than the quantity in the cart
                if item.product.Quantity < item.quantity:
                    logger.warning(f"Product {item.product.ProductID} is out of stock")
                    return redirect('transaction:error')  # Redirect to an error page

                # Update product quantity
                # item.product.Quantity -= item.quantity
                item.product.save()
                logger.info(f"Product {item.product.ProductID} quantity updated")
                print(f"Product {item.product.ProductID} quantity updated")

                # Delete the CartItem instance after updating product quantity
                item.delete(update_product_quantity=False)
                logger.info(f"CartItem {item.id} deleted")
                print(f"CartItem {item.id} deleted")

            # Create a new Cart instance for the customer
            print("About to create new instance of the cart")
            new_cart = Cart(customer=request.user.customer, total=0.00)
            new_cart.save()

    except Exception as e:
        # Handle the exception
        logger.error(f"An error occurred: {e}")
        return redirect('transaction:error')  # Redirect to an error page
    #potential fix for clicking back button

    request.session['payment_confirmed'] = True
    # Redirect to the success page
    return redirect('transaction:payment_successful')


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

    # Check if a rating by the current customer exists for each product
    ratings = ProductReview.objects.filter(CustomerID=customer.id, ProductID=OuterRef('ProductID'))
    order_history = order_history.annotate(has_rated=Exists(ratings))

    context = {
        'order_history': order_history,
    }

    return render(request, 'transaction/order_history.html', context)

def payment_successful(request):
    return render(request, 'transaction/payment/payment_successful.html')


