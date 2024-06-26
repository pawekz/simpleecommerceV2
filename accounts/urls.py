from django.urls import path
from . import views

app_name = 'accounts'

# in short, if you want to access the customer_register view, you will need to go to /accounts/register/customer/ or
# http://127.0.0.1/accounts/register/customer/
# http://127.0.0.1/accounts/login/
urlpatterns = [

    #path('seller_homepage/', views.seller_homepage, name='seller_homepage'),
    #path('customer_homepage/', views.customer_homepage, name='customer_homepage'),
    path('register/customer/', views.customer_register, name='customer_register'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('customer_updateregpage/', views.customer_updateregpage, name='customer_updateregpage'),
    path('seller_profile/', views.seller_profile, name='seller_profile'),
    path('seller_updateregpage/', views.seller_updateregpage, name='seller_updateregpage'),
    path('register/seller/', views.seller_register, name='seller_register'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('deactivate_account/', views.deactivate_account, name='deactivate_account'),
    path('reactivate_account/', views.reactivate_account, name='reactivate_account'),
    path('', views.main_menu, name='main_menu'),
    #path('', views.home, name='home'),
]
