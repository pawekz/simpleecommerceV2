from django.shortcuts import render, redirect
from . import views
from django.shortcuts import redirect
from products.models import Product
from .models import Cart
from accounts.models import Customer, CustomUser

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch all items in the customer's cart
    cart_items = Cart.objects.filter(customer=customer)

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'cart/cart.html', context)
#def cart_view(request):
#    if not request.user.is_authenticated:
#        return redirect('accounts:login')  # Redirect non-authenticated users
#
#    cart_items = Cart.objects.filter(user=request.user)  # Fetch all items in the user's cart
#
#    context = {
#       'cart_items': cart_items,
#    }
#
 #   return render(request, 'cart/cart.html', context)






def add_to_cart(request):
    product_id = request.POST.get('product_id')
    if product_id:  # check if product_id is not empty
        product = Product.objects.get(ProductID=product_id)
        custom_user = CustomUser.objects.get(username=request.user.username)  # get the CustomUser object for the current user
        customer, created = Customer.objects.get_or_create(customuser_ptr=custom_user)  # get or create a Customer object for the current CustomUser
        cart, created = Cart.objects.get_or_create(customer=customer)  # get or create a Cart object for the current customer
        cart.products.add(product)  # add the product to the cart
    return redirect('main_menu')