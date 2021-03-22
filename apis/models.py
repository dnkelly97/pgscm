from django.db import models
from rest_framework_api_key.models import AbstractAPIKey
from rest_framework_api_key.crypto import KeyGenerator
from rest_framework_api_key.models import BaseAPIKeyManager

# Create your models here.
class APIKeyManager(BaseAPIKeyManager):
    key_generator = KeyGenerator(prefix_length=8, secret_key_length=32)

class APIKey(AbstractAPIKey):
    objects = APIKeyManager()
    email = models.EmailField(max_length=255, unique=True)
