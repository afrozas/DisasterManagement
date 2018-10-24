from django.db import models


class Request(models.Model):
    keywords = models.CharField(max_length=200) # JSON string of list of keywords
    latitude = models.DecimalField(max_digits=10, decimal_places=5)
    longitude = models.DecimalField(max_digits=10, decimal_places=5)
    description = models.CharField(max_length=500)