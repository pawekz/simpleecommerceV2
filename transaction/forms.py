from django import forms
from .models import Transaction, OrderHistory

class UpdateOrderStatusForm(forms.Form):
    order = forms.ModelChoiceField(queryset=OrderHistory.objects.all())
    status = forms.ChoiceField(choices=Transaction.STATUS_CHOICES)