from django.shortcuts import render


# Create your views here.
def home(request):
    # add a functionality that chooses the preferred delivery method
    # (see `standard_delivery`, `express_delivery`, `next_day_delivery`)
    # code below

    return render(request, 'delivery/options.html')


def standard_delivery(request):
    # add a functionality that adds the total price of the products in the
    # cart + the standard delivery fee of 50.00
    # code below

    return render(request, 'delivery/standard_delivery.html')


def express_delivery(request):
    # add a functionality that adds the total price of the products in the
    # cart + the express delivery fee of 150.00
    #code below

    return render(request, 'delivery/express_delivery.html')


def next_day_delivery(request):
    # add a functionality that adds the total price of the products in the
    # cart + the express delivery fee of 150.00
    # code below

    return render(request, 'delivery/next_day_delivery.html')
