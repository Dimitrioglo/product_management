from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=13, help_text="Stock Keeping Unit")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name
