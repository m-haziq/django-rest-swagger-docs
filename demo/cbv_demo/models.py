from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=22)
    phone = models.CharField(max_length=22)
    address = models.CharField(max_length=44)