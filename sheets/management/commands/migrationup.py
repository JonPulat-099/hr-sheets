import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from sheets.models import Organization
from sheets.services.google.create_spreadsheet import create_spreadsheet_organization

load_dotenv()


class Command(BaseCommand):
    help = "Fetch & save country data"

    def handle(self, *args, **options):
        self.stdout.write("🟢 Command runned successfully")
        try:

            organizations = Organization.objects.all()
            for organization in organizations:
                sheet_url = create_spreadsheet_organization(organization)
                organization.sheet_url = sheet_url
                organization.save()

        except Exception as e:
            self.stdout.write(f"❌ Failed: {e}")

        self.stdout.write("🔵 Command completed")
