from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomerRegistrationForm, SellerRegistrationForm, CustomerProfileForm, SellerProfileForm
from django.contrib import messages

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'accounts/customer_registration.html', {'form': form})


def seller_register(request):
    if request.method == 'POST':
        form = SellerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:home')
    else:
        form = SellerRegistrationForm()
    return render(request, 'accounts/seller_registration.html', {'form': form})


def terms_and_conditions(request):
    return render(request, 'accounts/terms_and_conditions.html')


def home(request):
    return render(request, 'accounts/home.html')


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
                    return redirect('accounts:seller_profile')  # Redirect to the seller profile page
                else:
                    return redirect('accounts:customer_profile')  # Redirect to the customer profile page
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:home')



def customer_profile(request):
    if not request.user.is_customer:
        return redirect('accounts:login')  # Redirect non-customers

    customer = request.user.customer  # Fetch the Customer instance

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:customer_profile')
    else:
        form = CustomerProfileForm(instance=customer)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/customer_profile.html', {'form': form, 'password_form': password_form, 'customer': customer})



from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import CustomerProfileForm
from django.shortcuts import render, redirect

def customer_updateregpage(request):
    if not request.user.is_customer:
        return redirect('accounts:login')  # Redirect non-customers

    customer = request.user.customer  # Fetch the Customer instance

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            if password_form.is_valid():  # Check if the PasswordChangeForm is filled
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:customer_profile')  # Redirect to the customer profile page after update
        else:
            messages.error(request, 'Error updating profile. Please check your input.')  # Add this line
    else:
        form = CustomerProfileForm(instance=customer)  # Pre-fill the form with the current customer's information
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/customer_updateregpage.html', {'form': form, 'password_form': password_form, 'customer': customer})


def seller_profile(request):
    if not request.user.is_seller:
        return redirect('accounts:seller_profile')  # Redirect non-sellers

    seller = request.user.seller  # Fetch the Seller instance

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=seller)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:seller_profile')
    else:
        form = SellerProfileForm(instance=seller)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/seller_profile.html', {'form': form, 'password_form': password_form, 'seller': seller})

def seller_updateregpage(request):
    if not request.user.is_seller:
        return redirect('accounts:seller_profile')  # Redirect non-sellers

    seller = request.user.seller  # Fetch the Seller instance

    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=seller)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:seller_profile')  # Redirect to the seller profile page after update
    else:
        form = SellerProfileForm(instance=seller)  # Pre-fill the form with the current seller's information
        password_form = PasswordChangeForm(request.user)

    return render(request, 'accounts/seller_updateregpage.html', {'form': form, 'password_form': password_form, 'seller': seller})