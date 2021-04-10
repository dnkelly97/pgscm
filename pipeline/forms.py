from django.forms import forms
from pipeline.models import Pipeline, Stage, SavedQuery
from django.forms import ModelForm, Textarea, widgets, ModelMultipleChoiceField
from django.db.models import Q

class CreatePipelineForm(ModelForm):
    sources = ModelMultipleChoiceField(widget=widgets.CheckboxSelectMultiple(),
                                       queryset=SavedQuery.objects.all())

    class Meta:
        model = Pipeline
        fields = ['sources', 'name', 'num_stages', 'description', ]
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'cols': 40})
        }


class UpdatePipelineForm(ModelForm):
    # todo: Add model multiple choice fields for add_sources and delete sources. The tricky part will be defining the query_set
    add_sources = ModelMultipleChoiceField(widget=widgets.CheckboxSelectMultiple(), queryset=None, required=False)
    remove_sources = ModelMultipleChoiceField(widget=widgets.CheckboxSelectMultiple(), queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pipeline = kwargs.get('instance')
        if pipeline:
            self.fields['add_sources'].queryset = SavedQuery.objects.all().difference(pipeline.sources.all())
            self.fields['remove_sources'].queryset = pipeline.sources.all()
        else:
            raise ValueError("No pipeline instance given")

    class Meta:
        model = Pipeline
        fields = ['name', 'description']
        widgets = {
            'description': Textarea(attrs={'rows': 3, 'cols': 40})
        }


class UpdateStageForm(ModelForm):
    class Meta:
        model = Stage
        fields = ['name', 'stage_number', 'time_window', 'advancement_condition', 'pipeline']
