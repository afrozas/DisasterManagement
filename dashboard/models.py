from django.db import models


class Request(models.Model):
    person_name = models.CharField(max_length=50, blank=True)
    keywords = models.CharField(max_length=200)  # CSV of keywords
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    description = models.CharField(max_length=500, blank=True)
    phone_num = models.CharField(max_length=15, blank=True)
    donation = models.BooleanField(default=False)
