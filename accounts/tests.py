from django.test import TestCase, Client
from django.test import CustomUser, Customer, Seller
from django.urls import reverse


# Create your tests here.

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
        self.assertRedirects(response, reverse('home'))

        # Check if user was created
        user_exists = CustomUser.objects.filter(username='testuser').exists()
        self.assertTrue(user_exists)

        # Check if seller was created
        seller_exists = Seller.objects.filter(seller_name='Test User').exists()
        self.assertTrue(seller_exists)
