from django.contrib.postgres.fields import ArrayField
from django.db import models

import uuid

from customer.models import Customer

# Create your models here.

class Container(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    foods = models.JSONField(verbose_name="foods and counter")