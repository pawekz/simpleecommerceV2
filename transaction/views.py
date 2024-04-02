from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'payment/options.html')


def gcash_payment(request):
    return render(request, 'payment/gcash_payment.html')


def maya_payment(request):
    return render(request, 'payment/maya_payment.html')


def debit_payment(request):
    return render(request, 'payment/debit_payment.html')


def cod_payment(request):
    return render(request, 'payment/cod_payment.html')


def credit_payment(request):
    return render(request, 'payment/credit_payment.html')


def success(request):
    return render(request, 'payment/success.html')