from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Seller
from .forms import ProductForm
from .models import Product
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse



# Create your views here.
def home(request):
    return render(request, 'products/add_product.html')




def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.instance.SellerID = Seller.objects.get(username=request.user.username)
        if form.is_valid():
            try:
                product = form.save()
                # Fetch products that belong to the authenticated seller
                products = Product.objects.filter(SellerID=request.user.seller)
                return render(request, 'products/add_product.html', {'form': form, 'product': product, 'products': products})
            except Exception as e:
                messages.error(request, f"Error saving product: {e}")
        else:
            messages.error(request, f"Form is not valid. Errors: {form.errors}")
    else:
        form = ProductForm()
        # Fetch products that belong to the authenticated seller
        products = Product.objects.filter(SellerID=request.user.seller)
    return render(request, 'products/add_product.html', {'form': form, 'products': products})


def product_terms_and_conditions(request):
    return render(request, 'products/product_terms_and_conditions.html')



def edit_product(request, product_id):
    product = get_object_or_404(Product, ProductID=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:product_display')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form})



def delete_product(request, product_id):
    product = get_object_or_404(Product, ProductID=product_id)
    if request.method == 'POST':
        product.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def inventory(request):
    if request.user.is_authenticated:  # Check authentication first
        # Fetch all products that belong to the current seller
        products = Product.objects.filter(SellerID=request.user.seller)
        return render(request, 'products/inventory.html', {'products': products})
    return render(request, 'products/inventory.html')

def mark_as_sold(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, ProductID=product_id)
        product.is_sold = True  # Assuming you have an `is_sold` field in your Product model
        product.save()

        # Notify the seller here. The implementation depends on how you want to notify them.

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def checkout(request, product_id):
    quantity = int(request.GET.get('quantity', 1))  # Convert quantity to int
    product = get_object_or_404(Product, ProductID=product_id)
    product.Quantity = quantity  # Set the quantity
    product.TotalPrice = product.PricePerUnit * quantity  # Calculate the total price
    delivery_fee = 69
    total_amount = product.TotalPrice + delivery_fee
    return render(request, 'payment/checkoutpage.html', {'product': product, 'delivery_fee': delivery_fee, 'total_amount': total_amount})
def proceed_to_payment(request):
    # Implement your payment logic here
    return render(request, 'payment/options.html')