from django.db import models

# Create your models here.
class District(models.Model):
    division_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    bn_name = models.CharField(max_length=100)
    lat = models.CharField(max_length=20)
    long = models.CharField(max_length=20)