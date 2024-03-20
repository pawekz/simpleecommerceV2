from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, Seller, CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm


class CustomerRegistrationForm(UserCreationForm):
    customer_name = forms.CharField(label='Customer Name')
    contact_no = forms.CharField(label='Contact Number')
    address = forms.CharField(label='Address')

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('customer_name', 'contact_no', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.customer_name = self.cleaned_data['customer_name']
        user.contact_no = self.cleaned_data['contact_no']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user


class SellerRegistrationForm(UserCreationForm):
    seller_name = forms.CharField(label='Seller Name')
    stall_name = forms.CharField(label='Stall Name')
    contact_no = forms.CharField(label='Contact Number')
    address = forms.CharField(label='Address')

    class Meta(UserCreationForm.Meta):
        model = Seller
        fields = UserCreationForm.Meta.fields + ('seller_name', 'stall_name', 'contact_no', 'address')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.seller_name = self.cleaned_data['seller_name']
        user.stall_name = self.cleaned_data['stall_name']
        user.contact_no = self.cleaned_data['contact_no']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustomerProfileForm(UserChangeForm):
    password = None  # This will remove the password field from the form
    username = forms.CharField(max_length=20, disabled=True)

    class Meta:
        model = Customer
        fields = ['username', 'customer_name', 'contact_no', 'address']


class SellerProfileForm(UserChangeForm):
    password = None  # This will remove the password field from the form
    username = forms.CharField(max_length=20, disabled=True)

    class Meta:
        model = Seller
        fields = ['username', 'seller_name', 'stall_name', 'contact_no', 'address']
