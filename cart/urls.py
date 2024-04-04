from django.urls import path
from .views import cart_view, add_to_cart  # make sure add_to_cart view is imported
from accounts.views import main_menu  # import main_menu from accounts.views

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart'),
    path('add/', add_to_cart, name='add_to_cart'),  # new URL pattern for add_to_cart view
    path('main_menu/', main_menu, name='main_menu'),  # use main_menu from accounts.views
]