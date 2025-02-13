import os
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from sheets.models import Config
from sheets.services.google.get_all_sheets_value import get_sheets
from sheets.services.google.auth import spreadsheet_service

load_dotenv()


class Command(BaseCommand):
    help = "Fetch & save country data"

    def handle(self, *args, **options):
        self.stdout.write("🟢 Command runned successfully")
        try:
            spreadsheet_id = Config.objects.get(key="sheet_id").value
            sheets = get_sheets(spreadsheet_id)
            # print("sheets -> , ", sheets)

            request = []

            for sheet in sheets:
                title = sheet["properties"]["title"]
                sheet_id = sheet["properties"]["sheetId"]
                if (
                    title != "vacancies_all"
                    and title != "candidates_all"
                    and title != "employees_all"
                ):
                    request.append({"deleteSheet": {"sheetId": sheet_id}})

            if len(request) > 0:
                spreadsheet_service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id, body={"requests": request}
                ).execute()

        except Exception as e:
            self.stdout.write(f"❌ Failed: {e}")

        self.stdout.write("🔵 Command completed")
