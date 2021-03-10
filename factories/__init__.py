import factory
from pipeline.models import Pipeline, SavedQuery


class PipelineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pipeline

    name = factory.Sequence(lambda n: f'Pipeline {n}')


class SavedQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SavedQuery

    name = factory.Sequence(lambda n: f'Query {n}')
