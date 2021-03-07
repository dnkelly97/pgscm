from django.core.management import BaseCommand
from factories import PipelineFactory


from pipeline.models import Pipeline


ALREADY_LOADED_ERROR_MESSAGE = """
Data has already been loaded."""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads example pipeline data into the database"

    def handle(self, *args, **options):
        if Pipeline.objects.exists():
            print(ALREADY_LOADED_ERROR_MESSAGE)
        else:
            for i in range(3):
                pipeline = PipelineFactory.create()
                print("Pipeline created:", pipeline.name)
