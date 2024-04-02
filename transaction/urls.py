from django.urls import path
from . import views


app_name = 'transaction'

urlpatterns = [
    path('', views.home, name='home'),
    path('gcash_payment/', views.gcash_payment, name='gcash_payment'),
    path('maya_payment/', views.maya_payment, name='maya_payment'),
    path('debit_payment/', views.debit_payment, name='debit_payment'),
    path('cod_payment/', views.cod_payment, name='cod_payment'),
    path('credit_payment/', views.credit_payment, name='credit_payment'),
    path('success/', views.success, name='success'),

]
