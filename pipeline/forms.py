from django.forms import ModelForm
from pipeline.models import Pipeline


class CreateForm(ModelForm):
    class Meta:
        model = Pipeline
        fields = ['name', 'num_stages',
                  ]
