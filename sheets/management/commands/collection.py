from sheets.services.google.collection_sheets import collection
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Fetch & save country data"

    def handle(self, *args, **options):
        self.stdout.write("🟢 Command runned successfully")
        try:
            collection()
        except Exception as e:
            self.stdout.write(f"❌ Failed: {e}")

        self.stdout.write("🔵 Command completed")