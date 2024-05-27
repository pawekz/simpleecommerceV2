from django.http import Http404
from django.shortcuts import render, redirect
from accounts.models import Customer, CustomUser
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages
from decimal import Decimal


def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the latest cart for the current customer or create a new one if it doesn't exist
    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        cart = Cart.objects.create(customer=customer, total=0.00)

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

    return render(request, 'cart/cart.html', context)


def add_to_cart(request, product_id):
    print("add_to_cart view was called")  # Debug print statement
    print(f"Adding product with ID {product_id} to cart")  # Debug print statement

    if request.method != 'POST':
        print("Request method is not POST")
        return redirect('accounts:main_menu')

    print(f"Request POST data: {request.POST}")  # Debug print statement

    product = get_object_or_404(Product, ProductID=product_id)
    print(f"Product quantity: {product.Quantity}")  # Debug print statement
    print(f"Product price per unit: {product.PricePerUnit}")  # Debug print statement

    customer = Customer.objects.get(customuser_ptr_id=request.user.id)
    print(f"Customer: {customer}")  # Debug print statement

    cart_id = request.session.get('cart_id')
    if cart_id is None:
        cart = Cart.objects.create(customer=customer, total=0.00)
        request.session['cart_id'] = cart.id
        print(f"Created new cart with ID: {cart.id}")  # Debug print statement
    else:
        cart = Cart.objects.get(id=cart_id)
        print(f"Using existing cart with ID: {cart_id}")  # Debug print statement

    # Check if the product is in stock
    if product.Quantity <= 0:
        print("Product is out of stock")  # Debug print statement
        messages.error(request, 'This product is out of stock.')
        return redirect('accounts:main_menu')

    # Get the quantity from the form data
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        print("Invalid quantity received")  # Debug print statement
        messages.error(request, 'Invalid quantity.')
        return redirect('accounts:main_menu')

    print(f"Requested quantity: {quantity}")  # Debug print statement

    # Check if the product quantity is less than the requested quantity
    if product.Quantity < quantity:
        print("Not enough stock for this product")  # Debug print statement
        messages.error(request, 'Not enough stock for this product.')
        return redirect('accounts:main_menu')

    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 0, 'total_amount': 0.00}
    )
    print(f"Cart item created: {created}, Quantity before: {cart_item.quantity}")  # Debug print statement

    # If the product is already in the cart, increment the quantity
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    # Calculate total_amount for the CartItem instance
    if product.PricePerUnit is not None:
        total_amount = round(product.PricePerUnit * cart_item.quantity, 2)
    else:
        total_amount = 0.00

    cart_item.total_amount = total_amount
    cart_item.save()

    # Decrease the product quantity
    product.Quantity -= quantity
    product.save()

    # Update the cart total
    cart.total = Decimal(cart.total) + Decimal(total_amount).quantize(Decimal('0.00'))  # Add the price of the added product to the cart total
    cart.save()

    print(f"Product added to cart. Cart total: {cart.total}")  # Debug print statement
    return redirect('cart:cart')



def increase_quantity(request, product_id):
    product = get_object_or_404(Product, ProductID=product_id)
    customer = Customer.objects.get(customuser_ptr_id=request.user.id)
    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        raise Http404("No Cart found for this customer.")
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Check if the product quantity is greater than the cart item quantity before increasing
    if product.Quantity > cart_item.quantity:
        cart_item.quantity += 1
        cart_item.total_amount += product.PricePerUnit
        cart_item.save()

        cart.total += product.PricePerUnit
        cart.save()

        # Decrease the product quantity
        product.Quantity -= 1
        product.save()

    return redirect('cart:cart')


def decrease_quantity(request, product_id):
    product = get_object_or_404(Product, ProductID=product_id)
    customer = Customer.objects.get(customuser_ptr_id=request.user.id)
    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        raise Http404("No Cart found for this customer.")
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.total_amount -= product.PricePerUnit
        cart_item.save()

        cart.total -= product.PricePerUnit
        cart.save()

        # Increase the product quantity
        product.Quantity += 1
        product.save()

    else:
        # If the cart item quantity is 1, delete the cart item and increase the product quantity
        product.Quantity += 1
        product.save()
        cart_item.delete()

    return redirect('cart:cart')


def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, ProductID=product_id)
    customer = Customer.objects.get(customuser_ptr_id=request.user.id)

    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        raise Http404("No Cart found for this customer.")

    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Store the quantity before deleting the cart item
    quantity = cart_item.quantity

    # Delete the CartItem before modifying the product quantity
    cart_item.delete()

    # Subtract the total_amount of the CartItem from the Cart total
    cart.total -= product.PricePerUnit * quantity
    cart.save()

    # Increase the product quantity
    product.Quantity += quantity
    product.save()

    messages.success(request, 'Product removed from cart.')
    return redirect('cart:cart')
