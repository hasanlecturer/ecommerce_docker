from django.db import models

class Address(models.Model):
    full_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    apartment = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        abstract = True