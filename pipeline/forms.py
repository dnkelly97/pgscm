from django.forms import ModelForm
from pipeline.models import Pipeline, Stage
from django.forms import ModelForm, Textarea


class CreatePipelineForm(ModelForm):
    class Meta:
        model = Pipeline
        fields = ['name', 'num_stages', 'description'
                  ]
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'cols': 40})
        }


class UpdateStageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'stage_number', 'time_window', 'advancement_condition', 'pipeline']
