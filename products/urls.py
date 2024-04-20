from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('product_terms_and_conditions/', views.product_terms_and_conditions, name='terms_and_conditions'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('inventory/', views.inventory, name='inventory'),
    path('mark-as-sold/<int:product_id>/', views.mark_as_sold, name='mark_as_sold'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout'),
    path('proceed_to_payment/', views.proceed_to_payment, name='proceed_to_payment'),
]
