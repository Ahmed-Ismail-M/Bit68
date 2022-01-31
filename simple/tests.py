from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from simple.serializers import ProductSerializer

from simple.models import Product
# Create your tests here.

User = get_user_model()

class RegisterationTest(APITestCase):
    def test_registeration(self):
        data = {
            "username":"ahmed", "email":"ahmed@im-software.net", "password":"testpass"
        }
        response = self.client.post("/register", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # assert the registeration completed

class LoginTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="ahmed", email="ahmed@im-software.net", password="testpass")

    def test_login(self):
        data = {
            "username":"ahmed","password":"testpass"
        }
        response = self.client.post("/login", data)
        self.assertEqual(response.url, "/products") # assert the redirection to products url in case login success

class ProductTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="ahmed", email="ahmed@im-software.net", password="testpass")
        self.product = Product.objects.create(name="testproduct",price=50, seller=self.user)
        self.product_serialzer = ProductSerializer(self.product)
    def test_products(self):
     
        response = self.client.get("/products")
        self.assertEqual(response.json()[0], self.product_serialzer.data) # assert response data = product data

