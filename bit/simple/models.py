from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Product(models.Model):
    """ create a product model """
    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
