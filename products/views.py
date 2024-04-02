from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Seller
from .forms import ProductForm


# Create your views here.
def home(request):
    return render(request, 'products/product_display.html')


def product_display(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        form.instance.SellerID = Seller.objects.get(username=request.user.username)
        if form.is_valid():
            try:
                product = form.save()
                return redirect('products:product_display')
            except Exception as e:
                messages.error(request, f"Error saving product: {e}")
        else:
            messages.error(request, f"Form is not valid. Errors: {form.errors}")
    else:
        form = ProductForm()
    return render(request, 'products/product_display.html', {'form': form})

def product_terms_and_conditions(request):
    return render(request, 'products/product_terms_and_conditions.html')
