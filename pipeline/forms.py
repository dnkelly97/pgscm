from django.forms import forms
from pipeline.models import Pipeline, Stage, SavedQuery
from django.forms import ModelForm, Textarea, widgets


class CreatePipelineForm(ModelForm):
    class Meta:
        model = Pipeline
        fields = ['source', 'name', 'num_stages', 'description',
                  ]
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'cols': 40})
        }

    def __init__(self, *args, **kwargs):
        super(CreatePipelineForm, self).__init__(*args, **kwargs)
        self.fields["source"].widget = widgets.CheckboxSelectMultiple()
        self.fields["source"].help_text = ""
        self.fields["source"].queryset = SavedQuery.objects.all()


class UpdateStageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'stage_number', 'time_window', 'advancement_condition', 'pipeline']
