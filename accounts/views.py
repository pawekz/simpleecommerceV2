from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, get_user_model
from .forms import CustomerRegistrationForm, SellerRegistrationForm
from django.contrib import messages
from .forms import CustomerProfileUpdateForm, SellerProfileUpdateForm
from django.shortcuts import render, redirect
from .models import Customer, Seller
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from products.models import Product
from accounts.forms import SearchForm
from django.contrib.auth import login,  get_user_model
from .forms import UserRegistrationForm
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import forms
from django.contrib.auth.backends import ModelBackend




class AllowInactiveUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:main_menu')
                else:
                    form.add_error(None, 'This account has been deactivated.')
                    return render(request, 'accounts/login.html', {'form': form})
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            Cart.objects.create(user=user)  # create a Cart object for the new user
            return redirect('main_menu')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:main_menu')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/customer_registration.html', {'form': form})

def seller_register(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:main_menu')
    else:
        form = SellerRegistrationForm()
    return render(request, 'accounts/seller_registration.html', {'form': form})



@login_required
def deactivate_account(request):
    user = request.user
    user.is_active = False
    user.save()
    messages.add_message(request, messages.INFO, 'Your account has been deactivated.')

    # Check if the user is a customer before trying to access their cart
    if hasattr(user, 'customer'):
        # Clear the user's cart and update product quantities
        try:
            cart = Cart.objects.get(customer=user.customer)
            print(f"Found cart {cart.id} for customer {user.customer.id}")
            for item in cart.cartitem_set.all():
                print(f"Updating quantity for product {item.product.ProductID}")
                item.product.Quantity += item.quantity
                item.product.save()
            cart.cartitem_set.all().delete()
        except Cart.DoesNotExist:
            print(f"No cart found for customer {user.customer.id}")

    logout(request)
    return redirect('accounts:login')


def reactivate_account(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    messages.success(request, "Your account has been reactivated.")
                    return redirect('accounts:login')
                else:
                    form.add_error(None, 'Invalid username or password')
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/reactivate_account.html', {'form': form})

def terms_and_conditions(request):
    return render(request, 'accounts/terms_and_conditions.html')

def logout_view(request):
    logout(request)
    return redirect('accounts:login')


def customer_profile(request):
    # Get the Customer object for the current user
    customer = Customer.objects.get(customuser_ptr=request.user)

    # Fetch the latest cart for the current customer or create a new one if it doesn't exist
    cart = Cart.objects.filter(customer=customer).order_by('-id').first()
    if cart is None:
        cart = Cart.objects.create(customer=customer, total=0.00)

    # Fetch the recent 2 items added to the cart
    recent_cart_items = CartItem.objects.filter(cart=cart).order_by('-id')[:2]

    context = {
        'customer': customer,
        'recent_cart_items': recent_cart_items,
    }

    return render(request, 'accounts/customer_profile.html', context)

def customer_updateregpage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    customer = Customer.objects.get(username=request.user.username)  # Fetch the latest data from the database

    if request.method == 'POST':
        form = CustomerProfileUpdateForm(request.POST, instance=customer)
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not check_password(old_password, request.user.password):
            form.add_error('old_password', 'Incorrect password')
            print("Incorrect old password")  # Debug print statement
        elif new_password and confirm_password:
            if new_password != confirm_password:
                form.add_error('new_password', 'New password and confirm password do not match')
                print("New password and confirm password do not match")  # Debug print statement
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Important!
                print("Password updated successfully")  # Debug print statement
                return redirect('accounts:login')  # Redirect to the login page after password update
        elif form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            print("Form is valid, redirecting to customer_profile")  # Debug print statement
            return redirect('accounts:customer_profile')  # Redirect back to the customer_profile view
        else:
            print("Form is not valid")  # Debug print statement
            print(form.errors)  # Print form errors
    else:
        form = CustomerProfileUpdateForm(instance=customer)

    context = {
        'form': form,
        'customer': customer,
    }

    return render(request, 'accounts/customer_updateregpage.html', context)

def seller_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    seller = Seller.objects.get(username=request.user.username)  # Fetch the latest data from the database

    # Fetch the two most recent products added by the current seller
    recent_products = Product.objects.filter(SellerID=seller).order_by('-date_added')[:2]

    context = {
        'seller': seller,
        'recent_products': recent_products,
    }

    return render(request, 'accounts/seller_profile.html', context)

def seller_updateregpage(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    seller = Seller.objects.get(username=request.user.username)  # Fetch the latest data from the database

    if request.method == 'POST':
        form = SellerProfileUpdateForm(request.POST, instance=seller)
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not check_password(old_password, request.user.password):
            form.add_error('old_password', 'Incorrect password')
            print("Incorrect old password")  # Debug print statement
        elif new_password and confirm_password:
            if new_password != confirm_password:
                form.add_error('new_password', 'New password and confirm password do not match')
                print("New password and confirm password do not match")  # Debug print statement
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Important!
                print("Password updated successfully")  # Debug print statement
                return redirect('accounts:login')  # Redirect to the login page after password update
        elif form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            print("Form is valid, redirecting to seller_profile")  # Debug print statement
            return redirect('accounts:seller_profile')  # Redirect back to the seller_profile view
        else:
            print("Form is not valid")  # Debug print statement
            print(form.errors)  # Print form errors
    else:
        form = SellerProfileUpdateForm(instance=seller)

    context = {
        'form': form,
        'seller': seller,
    }

    return render(request, 'accounts/seller_updateregpage.html', context)

def main_menu(request):
    form = SearchForm(request.GET)
    if request.user.is_authenticated:
        if request.user.is_seller:
            # If the user is a seller, fetch only the products that belong to them
            products = Product.objects.filter(SellerID=request.user.seller)
            user_type = 'seller'
        else:
            # If the user is a customer, fetch all products
            products = Product.objects.all()
            user_type = 'customer'
    else:
        # If the user is a guest, fetch all products
        products = Product.objects.all()
        user_type = 'guest'

    if form.is_valid():
        query = form.cleaned_data['query']
        products = products.filter(ProductName__icontains=query)
        if not products:
            messages.info(request, f"No products found for '{query}'.")

    return render(request, 'accounts/main_menu.html', {'products': products, 'user_type': user_type})