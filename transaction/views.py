from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'transaction/options.html')


def gcash_payment(request):
    return render(request, 'transaction/payment/gcash_payment.html')


def maya_payment(request):
    return render(request, 'transaction/payment/maya_payment.html')


def cod_payment(request):
    return render(request, 'transaction/payment/cod_payment.html')


def credit_payment(request):
    return render(request, 'transaction/payment/credit_payment.html')


def success(request):
    return render(request, 'transaction/payment/success.html')