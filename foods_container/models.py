from django.contrib.postgres.fields import ArrayField
from django.db import models

import uuid

from customer.models import Customer

# Create your models here.

class Container(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="container name", max_length=50)
    foods = models.JSONField(verbose_name="foods and counter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)