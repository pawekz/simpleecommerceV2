from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('product_display/', views.product_display, name='product_display'),
    path('product_terms_and_conditions/', views.product_terms_and_conditions, name='terms_and_conditions'),



]