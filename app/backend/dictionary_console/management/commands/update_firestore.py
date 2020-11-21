from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "update firestore"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
