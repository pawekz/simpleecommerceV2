from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

from .forms import CustomerRegistrationForm, SellerRegistrationForm, CustomerProfileForm, SellerProfileForm


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
                return redirect('accounts:home_dashboard')  # Redirect to a success page.
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:home')


def profile_view(request):
    if request.user.is_customer:
        ProfileForm = CustomerProfileForm
        template_name = 'accounts/customer_profile.html'
        instance = request.user.customer
    elif request.user.is_seller:
        ProfileForm = SellerProfileForm
        template_name = 'accounts/seller_profile.html'
        instance = request.user.seller
    else:
        return redirect('accounts:home')  # Or handle this case differently

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=instance)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:home')
    else:
        form = ProfileForm(instance=instance)
        password_form = PasswordChangeForm(request.user)

    return render(request, template_name, {'form': form, 'password_form': password_form})


def home_dashboard(request):
    return render(request, 'accounts/home_dashboard.html')


def customer_profile(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:home_dashboard')
    else:
        form = CustomerProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'accounts/customer_profile.html', {'form': form, 'password_form': password_form})


def seller_profile(request):
    if request.method == 'POST':
        form = SellerProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('accounts:home_dashboard')
    else:
        form = SellerProfileForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
    return render(request, 'accounts/seller_profile.html', {'form': form, 'password_form': password_form})