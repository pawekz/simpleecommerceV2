# accounts/tests/test_customer.py

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, Customer

class CustomerRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:customer_register')

    def test_customer_registration(self):
        # Prepare data for POST request
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'customer_name': 'Test User',
            'contact_no': '1234567890',
            'address': 'Test Address'
        }

        # Send POST request to customer_register view
        response = self.client.post(self.register_url, data)

        # Check if user was redirected to 'home' after successful registration
        self.assertRedirects(response, reverse('home'))

        # Check if user was created
        user_exists = CustomUser.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

        # Check if customer was created
        customer_exists = Customer.objects.filter(customer_name='Test User').exists()
        self.assertTrue(customer_exists)