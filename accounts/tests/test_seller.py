# accounts/tests/test_seller.py

from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import CustomUser, Seller

class SellerRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:seller_register')

    def test_seller_registration(self):
        # Prepare data for POST request
        data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'seller_name': 'Test User',
            'stall_name': 'Test Stall',
            'contact_no': '1234567890',
            'address': 'Test Address'
        }

        # Send POST request to seller_register view
        response = self.client.post(self.register_url, data)

        # Check if user was redirected to 'home' after successful registration
        self.assertRedirects(response, reverse('accounts:home_dashboard'))

        # Check if user was created
        user_exists = CustomUser.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

        # Check if seller was created
        seller_exists = Seller.objects.filter(seller_name='Test User').exists()
        self.assertTrue(seller_exists)