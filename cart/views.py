from django.shortcuts import render, redirect
from accounts.models import Customer, CustomUser
from django.shortcuts import get_object_or_404, redirect
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the cart for the current customer or create a new one if it doesn't exist
    cart, created = Cart.objects.get_or_create(customer=customer, defaults={'total': 0.00})

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
    product = get_object_or_404(Product, ProductID=product_id)
    customer = Customer.objects.get(customuser_ptr_id=request.user.id)
    cart, created = Cart.objects.get_or_create(customer=customer, defaults={'total': 0})

    # Check if the product is in stock
    if product.Quantity <= 0:
        messages.error(request, 'This product is out of stock.')
        return redirect('accounts:main_menu')

    # Get the quantity from the form data
    quantity = int(request.POST.get('quantity', 1))

    # Check if the product quantity is less than the requested quantity
    if product.Quantity < quantity:
        messages.error(request, 'Not enough stock for this product.')
        return redirect('accounts:main_menu')

    # Calculate total_amount before creating or getting the CartItem instance
    if product.PricePerUnit is not None:
        total_amount = product.PricePerUnit * quantity
    else:
        total_amount = 0

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity, 'total_amount': total_amount}
    )

    if not item_created:
        cart_item.quantity += quantity
        cart_item.total_amount += total_amount
        cart_item.save()

    # Decrease the product quantity
    product.Quantity -= quantity
    product.save()

    # Update the cart total
    cart.total += total_amount  # Add the price of the added product to the cart total
    cart.save()

    return redirect('cart:cart')



def increase_quantity(request, product_id):
    product = get_object_or_404(Product, ProductID=product_id)
    customer = Customer.objects.get(customuser_ptr_id=request.user.id)
    cart = get_object_or_404(Cart, customer=customer)
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
    cart = get_object_or_404(Cart, customer=customer)
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
    cart = get_object_or_404(Cart, customer=customer)

    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    # Subtract the total_amount of the CartItem from the Cart total
    cart.total -= cart_item.total_amount
    cart.save()

    # Increase the product quantity
    product.Quantity += cart_item.quantity
    product.save()

    # Delete the CartItem
    cart_item.delete()

    messages.success(request, 'Product removed from cart.')
    return redirect('cart:cart')
