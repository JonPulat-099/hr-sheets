from django.core.management.base import BaseCommand, CommandError
from sheets.services.google.create_spreadsheet import create_spreadsheet


class Command(BaseCommand):
    help = 'Create a Google Sheet'

    # TODO: try|catch block and handle exceptions

    def handle(self, *args, **options):
        self.stdout.write('🟢 Command runned successfully')
        result = create_spreadsheet()
        if result:
            self.stdout.write('✅ Command executed successfully')
        else:
            self.stdout.write('❌ Command failed')

        self.stdout.write('🔵 Command completed')