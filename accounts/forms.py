from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, PasswordChangeForm
from .models import Customer, Seller



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



class CustomerProfileUpdateForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Customer
        fields = ['customer_name', 'username', 'contact_no', 'address', 'old_password', 'new_password', 'confirm_password']




class SellerProfileUpdateForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput())
    new_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Seller
        fields = ['username', 'seller_name', 'contact_no', 'address', 'stall_name', 'old_password', 'new_password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError(
                    "New password and confirm password do not match"
                )