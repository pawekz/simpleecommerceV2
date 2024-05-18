from django.urls import path
from . import views


app_name = 'transaction'

urlpatterns = [
    path('', views.home, name='home'),
    path('payment_option/', views.payment_option, name='payment_option'),
    path('gcash_payment/', views.gcash_payment, name='gcash_payment'),
    path('maya_payment/', views.maya_payment, name='maya_payment'),
    path('cod_payment/', views.cod_payment, name='cod_payment'),
    path('credit_payment/', views.credit_payment, name='credit_payment'),
    path('review_cart/', views.review_cart, name='review_cart'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    path('success/', views.success, name='success'),
]
