from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help='prints a simple hello message'

    def handle(self, *args, **kwargs):
        self.stdout.write("👋 Hello from your custom command!")