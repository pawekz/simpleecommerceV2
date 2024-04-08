from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomerRegistrationForm, SellerRegistrationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomerProfileUpdateForm, SellerProfileUpdateForm
from django.shortcuts import render, redirect
from .models import Customer, Seller
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render
from products.models import Product
from accounts.forms import SearchForm
from django.contrib.auth import login
from .forms import UserRegistrationForm
from cart.models import Cart



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


def terms_and_conditions(request):
    return render(request, 'accounts/terms_and_conditions.html')


#def home(request):
#    form = SearchForm(request.GET)
#    products = Product.objects.all()  # Fetch all products
#    if form.is_valid():
#        query = form.cleaned_data['query']
#        products = products.filter(ProductName__icontains=query)
#        if not products.exists():
#            messages.warning(request, 'No products found for your query.')
#    return render(request, 'accounts/main_menu.html', {'form': form, 'products': products})




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_seller:  # Check if the user is a seller
                    return redirect('accounts:seller_homepage')  # Redirect to the seller profile page
                else:
                    return redirect('accounts:customer_homepage')  # Redirect to the customer profile page
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:main_menu')



def customer_profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # Redirect non-authenticated users

    customer = Customer.objects.get(username=request.user.username)  # Fetch the latest data from the database

    context = {
        'customer': customer,
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
    products = Product.objects.all()  # Fetch all products
    if form.is_valid():
        query = form.cleaned_data['query']
        products = products.filter(ProductName__icontains=query)
        if not products:
            messages.info(request, f"No products found for '{query}'.")
            return render(request, 'accounts/main_menu.html', {'form': form, 'products': products})


    return render(request, 'accounts/main_menu.html', {'products': products})
def customer_homepage(request):
    if request.user.is_authenticated:  # Check authentication first
        form = SearchForm(request.GET)
        products = Product.objects.all()  # Fetch all products

        if form.is_valid():
            query = form.cleaned_data['query']
            products = products.filter(ProductName__icontains=query)
            if not products:
                messages.info(request, f"No products found for '{query}'.")
                return render(request, 'accounts/customer_homepage.html', {'form': form, 'products': products})
        # No need to check authentication again as it's done at the beginning

        return render(request, 'accounts/customer_homepage.html', {'form': form, 'products': products})
    return render(request, 'accounts/customer_homepage.html')

def seller_homepage(request):
    if request.user.is_authenticated:  # Check authentication first
        form = SearchForm(request.GET)
        products = Product.objects.all()  # Fetch all products

        if form.is_valid():
            query = form.cleaned_data['query']
            products = products.filter(ProductName__icontains=query)
            if not products:
                messages.info(request, f"No products found for '{query}'.")
                return render(request, 'accounts/seller_homepage.html', {'form': form, 'products': products})
        # No need to check authentication again as it's done at the beginning

        return render(request, 'accounts/seller_homepage.html', {'form': form, 'products': products})
    return render(request, 'accounts/seller_homepage.html')
