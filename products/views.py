from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from accounts.models import Seller, Customer
from transaction.models import OrderHistory
from .forms import ProductForm
from .models import Product, ProductReview
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
                return render(request, 'products/add_product.html',
                              {'form': form, 'product': product, 'products': products})
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
            messages.success(request, "Product details have been successfully updated.")
            return redirect('products:redirection')
        else:
            messages.error(request, "Failed updating product details.")
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

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def checkout(request, product_id):
    quantity = int(request.GET.get('quantity', 1))  # Convert quantity to int
    product = get_object_or_404(Product, ProductID=product_id)
    product.Quantity = quantity  # Set the quantity
    product.TotalPrice = product.PricePerUnit * quantity  # Calculate the total price
    delivery_fee = 69
    total_amount = product.TotalPrice + delivery_fee
    return render(request, 'cart/checkoutpage.html',
                  {'product': product, 'delivery_fee': delivery_fee, 'total_amount': total_amount})


def proceed_to_payment(request):
    # Implement your payment logic here
    return render(request, 'delivery/delivery_option.html')


def redirection(request):
    return render(request, "products/redirection.html")

@require_POST
def add_review(request):
    product_id = request.POST.get('ProductID')
    product = get_object_or_404(Product, ProductID=product_id)
    customer_id = request.user.id

    # Retrieve the Customer instance
    customer = get_object_or_404(Customer, id=customer_id)

    # Check if a review already exists for this product by this customer
    existing_review = ProductReview.objects.filter(ProductID=product, CustomerID=customer).first()
    if existing_review:
        # If a review already exists, return a message to notify the customer
        return JsonResponse({'success': False, 'message': 'You have already reviewed this product.'})

    # If no review exists, create a new one
    ProductReview.objects.create(ProductID=product, CustomerID=customer, Rating=1)
    return JsonResponse({'success': True})

def review_product(request, product_id):
    order_histories = OrderHistory.objects.filter(ProductID=product_id)
    product = order_histories.first().ProductID if order_histories else None
    return render(request, 'products/review_product.html', {'product': product})
