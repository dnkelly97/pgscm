from django.forms import ModelForm
from pipeline.models import Pipeline, Stage


class CreateForm(ModelForm):
    class Meta:
        model = Pipeline
        fields = ['name', 'num_stages',
                  ]


class UpdateStageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'time_window', 'advancement_condition']
