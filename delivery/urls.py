from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('home/', views.home, name='home'),
path('delivery_option/', views.delivery_option, name='delivery_option'),
    # ...
]