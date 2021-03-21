from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

# Create your models here.
class APIKey(AbstractAPIKey):
    email = models.EmailField(max_length=255, unique=True)
