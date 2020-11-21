from django.core.management.base import BaseCommand

from app.backend.dictionary_console.models import Video


class Command(BaseCommand):
    help = "update firestore"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        pass
