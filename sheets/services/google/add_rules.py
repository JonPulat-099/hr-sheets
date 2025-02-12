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
        values.append({"userEnteredValue": f"{country.name_ru} [{country.iso_code}]"})

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
                            {"userEnteredValue": "Новый [new]"},
                            {"userEnteredValue": "В Процессе [progress]"},
                            {"userEnteredValue": "Одобрено [hired]"},
                            {"userEnteredValue": "Отказано [reject]"},
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
                                "userEnteredValue": f"='vacancies_all'!B2:B"
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


def add_rules_to_vacancies_sheet(spreadsheet_id, sheet_id, organization, has_top):
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

    if has_top:
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
                                {"userEnteredValue": "Да"},
                                {"userEnteredValue": "Нет"},
                            ],
                        },
                        "showCustomUi": True,
                        "inputMessage": "Это топ ваканыия ?",
                        "strict": False,
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


def update_rules_of_vacancies_sheet():
    from sheets.models import VacancyCategory, Organization

    categories = VacancyCategory.objects.all()
    
    values = []

    for category in categories:
        values.append({"userEnteredValue": category.name})


    organizations = Organization.objects.all()

    if (len(organizations) == 0):
        return

    for org in organizations:
        try:
            spreadsheet_id = str(org.sheet_url).split("/")[-1]
            sheets = get_sheets(spreadsheet_id)
            vacancy_sheet_id = None
            for sheet in sheets:
                if sheet["properties"]["title"] == "vacancies_all":
                    vacancy_sheet_id = sheet["properties"]["sheetId"]
                    break

            request = [
                {
                    "setDataValidation": {
                        "range": {
                            "sheetId": vacancy_sheet_id,
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
                            "strict": False,
                        },
                    }
                }
            ]

            body = {"requests": request}
            response = (
                spreadsheet_service.spreadsheets()
                .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
                .execute()
            )
        except Exception as e:
            print(f"❌ Failed: {e}")
            return
