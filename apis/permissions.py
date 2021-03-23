from rest_framework_api_key.permissions import BaseHasAPIKey
from .models import APIKey

class HasAPIKey(BaseHasAPIKey):
    model = APIKey
