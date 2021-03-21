from django.forms import ModelForm
from pipeline.models import Pipeline, Stage
from bootstrap_modal_forms.forms import BSModalModelForm


class CreateForm(ModelForm):
    class Meta:
        model = Pipeline
        fields = ['name', 'num_stages',
                  ]


class UpdateStageForm(BSModalModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'time_window', 'advancement_condition']
