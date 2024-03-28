from django.urls import path
from . import views

app_name = 'accounts'

# in short, if you want to access the customer_register view, you will need to go to /accounts/register/customer/ or
# http://127.0.0.1/accounts/register/customer/
# http://127.0.0.1/accounts/login/
urlpatterns = [
    path('home_dashboard/', views.home_dashboard, name='home_dashboard'),
    path('register/customer/', views.customer_register, name='customer_register'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('customer_updateregpage/', views.customer_updateregpage, name='customer_updateregpage'),
    path('register/seller/', views.seller_register, name='seller_register'),
    path('terms_and_conditions/', views.terms_and_conditions, name='terms_and_conditions'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('', views.home, name='home'),
]
