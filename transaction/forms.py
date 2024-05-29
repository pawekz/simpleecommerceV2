from django import forms
from .models import Transaction

class UpdateOrderStatusForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['status']