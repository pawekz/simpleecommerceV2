from django.urls import path
from .views import cart_view, add_to_cart, remove_from_cart, increase_quantity, decrease_quantity # make sure add_to_cart view is imported
from accounts.views import main_menu  # import main_menu from accounts.views
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/', add_to_cart, name='add_to_cart'),  # new URL pattern for add_to_cart view
    path('', main_menu, name='main_menu'),  # use main_menu from accounts.views
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:product_id>/', increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/', decrease_quantity, name='decrease_quantity'),
]
