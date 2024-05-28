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
    path('error/', views.error, name='error'),
    path('order_history/', views.order_history,name='order_history'),
    path('payment_successful/<int:transaction_id>/', views.payment_successful,name='payment_successful'),
    #path('track_delivery/<int:order_id>/', views.track_delivery, name='track_delivery'), #change
    path('seller_order_history/', views.seller_order_history, name='seller_order_history'),
    path('ajax_update_order_status/', views.ajax_update_order_status, name='ajax_update_order_status'),
    path('customer_trackdelivery/<int:transaction_id>/', views.customer_trackdelivery, name='customer_trackdelivery'), #track delivery button
]
