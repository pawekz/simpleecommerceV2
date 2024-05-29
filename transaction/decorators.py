from django.http import HttpResponse
from django.shortcuts import redirect

def customer_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_customer:
            return function(request, *args, **kwargs)
        else:
            return redirect('accounts:login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def seller_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_seller:
            return function(request, *args, **kwargs)
        else:
            return redirect('accounts:login')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap