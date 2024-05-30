
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('transaction/', include('transaction.urls')),
    path('delivery/', include('delivery.urls')),
    path('chat/', include(('chat.urls', 'chat'), namespace='chat')),

]

