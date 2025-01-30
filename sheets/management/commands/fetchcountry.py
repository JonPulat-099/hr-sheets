from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create a Google Sheet"

    # TODO: try|catch block and handle exceptions

    def handle(self, *args, **options):
        self.stdout.write("🟢 Command runned successfully")
        

        self.stdout.write("🔵 Command completed")
