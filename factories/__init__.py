import factory
import faker
from pipeline.models import Pipeline, SavedQuery


fake = faker.Faker()


class PipelineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pipeline

    name = factory.Sequence(lambda n: f'Pipeline {n}')


class SavedQueryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SavedQuery

    query_name = factory.Sequence(lambda n: f'Query {n}')
    description = factory.Sequence(lambda n: f'The {n}th factory generated saved query')
    query = {'gpa': '', 'name': fake.name(), 'degree': '',
             'gender': '', 'country': '', 'military': 'unknown',
             'ethnicity': '', 'university': '', 'school_year': '',
             'us_citizenship': 'unknown', 'first_generation': 'unknown'}
