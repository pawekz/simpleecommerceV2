from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    ProductName = forms.CharField(label='Product Name',
                                  max_length=128,
                                  error_messages={
                                      'required': 'Product Name is required',
                                      'invalid': 'Enter a valid value'
                                  })
    Description = forms.CharField(label='Description',
                                  max_length=255,
                                  error_messages={
                                      'required': 'Description is required, make it short and sweet',
                                      'invalid': 'Enter a valid description'
                                  })
    PricePerUnit = forms.DecimalField(label='Price Per Unit',
                                      max_digits=12,
                                      decimal_places=2,
                                      error_messages={
                                          'required': 'Price per unit is required',
                                          'invalid': 'Enter a valid price in decimal format example: 100.00'
                                      })
    Quantity = forms.IntegerField(label='Quantity',
                                  error_messages={
                                      'required': 'Quantity is required',
                                      'invalid': 'Enter a valid quantity'
                                  })
    image = forms.ImageField(label='Upload an image',
                             error_messages={
                                 'required': 'Image is required',
                                 'invalid': 'Upload a valid image'
                             })

    class Meta:
        model = Product
        fields = ['ProductName', 'Description', 'PricePerUnit', 'Quantity', 'image']


