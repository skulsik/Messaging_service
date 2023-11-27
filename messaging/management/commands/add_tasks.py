from django.core.management import BaseCommand

from services.celery_beat import AddTask


class Command(BaseCommand):
    def handle(self, *args, **options):
        AddTask()
