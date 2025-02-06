from .auth import spreadsheet_service
from .get_all_sheets_value import get_all
from sheets.models import Config


def collection():
    spreadsheet_id = Config.objects.get(key="sheet_id").value
    vacancies, canditates, employees = get_all()

    (
        spreadsheet_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"vacancies_all!A2",
            body={"values": vacancies},
            valueInputOption="RAW",
        )
        .execute()
    )

    (
        spreadsheet_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"candidates_all!A2",
            body={"values": canditates},
            valueInputOption="RAW",
        )
        .execute()
    )

    (
        spreadsheet_service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=f"employees_all!A2",
            body={"values": employees},
            valueInputOption="RAW",
        )
        .execute()
    )
