from django.test import TestCase
import requests
# Create your tests here.

data = {
    "username":"ahmed", "password":"super"
}
r = requests.post("http://127.0.0.1:8000/login", data=data)
print(r.text)