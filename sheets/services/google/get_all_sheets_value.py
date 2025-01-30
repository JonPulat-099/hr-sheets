from .auth import spreadsheet_service
from sheets.models import Config


def get_all():
    try:
        spreadsheet_id = Config.objects.get(key="sheet_id").value

        spreadsheet = (
            spreadsheet_service.spreadsheets()
            .get(spreadsheetId=spreadsheet_id)
            .execute()
        )

        sheets = spreadsheet.get("sheets")

        canditates = []
        vacancies = []

        for sheet in sheets:
            sheet_name = sheet["properties"]["title"]

            result = (
                spreadsheet_service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}")
                .execute()
            )

            values = result.get("values", [])

            if sheet_name.endswith("_candidates"):
                canditates += values[1:]
            elif sheet_name.endswith("_vacancies"):
                vacancies += values[1:]

        return vacancies, canditates

    except Exception as e:
        print(f"❌ Failed: {e}")
        return [], []
