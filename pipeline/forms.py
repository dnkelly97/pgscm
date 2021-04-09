from django.forms import forms
from pipeline.models import Pipeline, Stage, SavedQuery
from django.forms import ModelForm, Textarea, widgets, ModelMultipleChoiceField


class CreatePipelineForm(ModelForm):
    sources = ModelMultipleChoiceField(widget=widgets.CheckboxSelectMultiple(),
                                       queryset=SavedQuery.objects.all())

    class Meta:
        model = Pipeline
        fields = ['sources', 'name', 'num_stages', 'description', ]
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'cols': 40})
        }


class UpdateStageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'stage_number', 'time_window', 'advancement_condition', 'pipeline']
