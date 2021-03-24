from django.forms import ModelForm
from pipeline.models import Pipeline, Stage
from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm


class CreateForm(ModelForm):
    class Meta:
        model = Pipeline
        fields = ['name', 'num_stages',
                  ]


class UpdateStageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'stage_number', 'time_window', 'advancement_condition', 'pipeline']
