from sheets.services.google.auth import spreadsheet_service
from .get_all_sheets_value import get_sheets


def add_rule_to_candidate_sheet(spreadsheet_id, sheet_id, organization):
    from sheets.models import Country

    requests = []

    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3,
                    "startRowIndex": 1,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [
                            {"userEnteredValue": "Мужской [male]"},
                            {"userEnteredValue": "Женский [female]"},
                        ],
                    },
                    "showCustomUi": True,
                    "inputMessage": "Select from the list",
                    "strict": False,
                },
            }
        }
    )

    countires = Country.objects.all()
    values = []

    for country in countires:
        values.append(
            {"userEnteredValue": f"{country.name_ru} [{country.iso_code}]"})

    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": 3,
                    "endColumnIndex": 4,
                    "startRowIndex": 1,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": values,
                    },
                    "showCustomUi": True,
                    "inputMessage": "Select from the list",
                    "strict": False,
                },
            }
        }
    )

    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": 5,
                    "endColumnIndex": 6,
                    "startRowIndex": 1,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [
                            {
                                "userEnteredValue": "Новый [new]"
                            },
                            {
                                "userEnteredValue": "В Процессе [progress]"
                            },
                            {
                                "userEnteredValue": "Одобрено [hired]"
                            },
                            {
                                "userEnteredValue": "Отказано [reject]"
                            },
                        ],
                    },
                    "showCustomUi": True,
                    "inputMessage": "Select the status",
                    "strict": True,
                },
            }
        }
    )

    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": 7,
                    "endColumnIndex": 8,
                    "startRowIndex": 1,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [
                            {
                                "userEnteredValue": f"{organization.name} [{organization.org_code}]"
                            },
                        ],
                    },
                    "showCustomUi": True,
                    "inputMessage": "Select the organization name",
                    "strict": True,
                },
            }
        }
    )

    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": 6,
                    "endColumnIndex": 7,
                    "startRowIndex": 1,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_RANGE",
                        "values": [
                            {
                                "userEnteredValue": f"='{organization.org_code}_vacancies'!B2:B"
                            },
                        ],
                    },
                    "showCustomUi": True,
                    "inputMessage": "Select the vacancy name",
                    "strict": True,
                },
            }
        }
    )

    body = {"requests": requests}
    response = (
        spreadsheet_service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )


def add_rules_to_vacancies_sheet(spreadsheet_id, sheet_id, organization):
    requests = []

    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": 0,
                    "endColumnIndex": 1,
                    "startRowIndex": 1,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [
                            {
                                "userEnteredValue": f"{organization.name} [{organization.org_code}]"
                            },
                        ],
                    },
                    "showCustomUi": True,
                    "inputMessage": "Select the organization name",
                    "strict": True,
                },
            }
        }
    )

    body = {"requests": requests}
    response = (
        spreadsheet_service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )


def update_rules_of_vacancies_sheet(spreadsheet_id):
    if spreadsheet_id is None:
        print('spreadsheet_id is None')
        return

    from sheets.models import VacancyCategory

    categories = VacancyCategory.objects.all()
    print('categories -> ', categories)
    values = []

    for category in categories:
        values.append({"userEnteredValue": category.name})

    sheets = get_sheets(spreadsheet_id)
    requests = []

    for sheet in sheets:
        sheet_name = sheet["properties"]["title"]
        if sheet_name.endswith("_vacancies"):
            sheet_id = sheet["properties"]["sheetId"]

            requests.append(
                {
                    "setDataValidation": {
                        "range": {
                            "sheetId": sheet_id,
                            "startColumnIndex": 2,
                            "endColumnIndex": 3,
                            "startRowIndex": 1,
                        },
                        "rule": {
                            "condition": {
                                "type": "ONE_OF_LIST",
                                "values": values,
                            },
                            "showCustomUi": True,
                            "inputMessage": "Select category",
                            "strict": True,
                        },
                    }
                }
            )

    body = {"requests": requests}
    response = (
        spreadsheet_service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )
