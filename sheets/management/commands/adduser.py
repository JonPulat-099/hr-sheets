import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

load_dotenv()
class Command(BaseCommand):
    help = "Fetch & save country data"

    def handle(self, *args, **options):
        self.stdout.write("🟢 Command runned successfully")
        try:
            User = get_user_model()
            User.objects.filter(username=os.getenv('ROOT_USER')).exists() or \
                User.objects.create_superuser(
                    os.getenv('ROOT_USER'), '', os.getenv('ROOT_PASSWORD'))
        except Exception as e:
            self.stdout.write(f"❌ Failed: {e}")

        self.stdout.write("🔵 Command completed")
