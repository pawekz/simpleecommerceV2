from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('home/', views.home, name='home'),
    # ...
]