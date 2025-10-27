from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.

class auth_view_test(TestCase):
    def setup(self):
        self.client = Client()
    
    def test_token_view(self):
        response = self.client.post(reverse(''),{
            'username': 'test',
            'password': '1234'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '')