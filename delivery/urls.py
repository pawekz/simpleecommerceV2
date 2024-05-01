from django.urls import path
from . import views
from delivery import views

app_name = 'delivery'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('delivery_option/', views.delivery_option, name='delivery_option'),
    # path('update_status', views.update_order_status, name='update_status'),
    path('seller_updateorderstatus/', views.seller_updateorderstatus, name='seller_updateorderstatus'),
    # ...
]