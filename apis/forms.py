from django.forms import ModelForm
from .models import APIKey

class CreateForm(ModelForm):
    class Meta:
        model = APIKey
        fields = ['name',
                  'email',
                  'expiry_date']