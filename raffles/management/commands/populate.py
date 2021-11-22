from django.core.management import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Populate database with required instances"

    def handle(self, *args, **options):
        pass
