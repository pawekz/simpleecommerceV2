from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('product_display/', views.product_display, name='product_display'),
    path('product_terms_and_conditions/', views.product_terms_and_conditions, name='terms_and_conditions'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),


]