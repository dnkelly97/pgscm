import factory
from pipeline.models import Pipeline, SavedQuery


class PipelineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pipeline

    name = factory.Sequence(lambda n: f'Pipeline {n}')
