from sheets.services.google.auth import spreadsheet_service
from sheets.services.google.add_rules import (
    add_rule_to_candidate_sheet,
    add_rules_to_vacancies_sheet,
)


def add_sheets_to_organization(organization, spreadsheet_id):
    requests = []
    sheets = [
        f"{organization.org_code}_vacancies",
        f"{organization.org_code}_candidates",
        f"{organization.org_code}_employees",
    ]

    requests.append(
        {
            "addSheet": {
                "properties": {
                    "title": sheets[0],
                },
            }
        }
    )
    requests.append(
        {
            "addSheet": {
                "properties": {
                    "title": sheets[1],
                },
            }
        }
    )
    requests.append(
        {
            "addSheet": {
                "properties": {
                    "title": sheets[2],
                },
            }
        }
    )
    body = {"requests": requests}

    # add sheets for organization
    new_sheets = (
        spreadsheet_service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )

    # add headers to the new sheets
    # vacancy_sheet_header
    vacancy_sheet_range_body = {
        "values": [
            [
                "Название организации",
                "Название вакансии",
                "Детали вакансии",
                "Зарплата",
                "Кол-во вакансий",
                "Топ вакансия",
            ],
            [
                f"{organization.name} [{organization.org_code}]",
                "Тест вакансия",
                "Подробности тестовой вакансии",
                "100000",
                "1",
                "Да",
            ],
        ]
    }

    # candidate_sheet_header
    candidate_sheet_range_body = {
        "values": [
            [
                "Полное имя кандидата",
                "Эл. почта кандидата",
                "Пол",
                "Гражданство",
                "Зарплата",
                "Статус",
                "Название вакансии",
                "Название организации",
            ],
        ]
    }

    employee_sheet_range_body = {
        "values": [
            [
                "Название организации",
                "Кол-во сотрудников",
                "Кол-во сотрудников (мужского пола)",
                "Кол-во сотрудников (женского пола)",
                "Всего экспатриантов",
            ]
        ]
    }

    vacancy_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={
        new_sheets['replies'][0]['addSheet']['properties']['sheetId']}"
    candidate_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={
        new_sheets['replies'][1]['addSheet']['properties']['sheetId']}"

    # add headers to the new sheets
    try:
        spreadsheet_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheets[0]}!A1",
            valueInputOption="RAW",
            body=vacancy_sheet_range_body,
        ).execute()
    except Exception as e:
        pass
        print("ERROR [ADD VACANCIES SHEET] =>", e)

    try:
        spreadsheet_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheets[1]}!A1",
            valueInputOption="RAW",
            body=candidate_sheet_range_body,
        ).execute()
    except Exception as e:
        pass
        print("ERROR [ADD CANDIDATE SHEET] =>", e)

    try:
        spreadsheet_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheets[2]}!A1",
            valueInputOption="RAW",
            body=employee_sheet_range_body,
        ).execute()

    except Exception as e:
        pass
        print("ERROR [ADD EMPLOYEES SHEET] =>", e)

    try:
        add_rule_to_candidate_sheet(
            spreadsheet_id,
            new_sheets["replies"][1]["addSheet"]["properties"]["sheetId"],
            organization,
        )
    except Exception as e:
        pass
        print("ERROR [ADD CANDIDATE RULES]", e)

    try:
        add_rules_to_vacancies_sheet(
            spreadsheet_id,
            new_sheets["replies"][0]["addSheet"]["properties"]["sheetId"],
            organization,
            True,
        )
    except Exception as e:
        pass
        print("ERROR [ADD VACANCIES RULES]", e)

    try:
        add_rules_to_vacancies_sheet(
            spreadsheet_id,
            new_sheets["replies"][2]["addSheet"]["properties"]["sheetId"],
            organization,
            False,
        )
    except Exception as e:
        pass
        print("ERROR [ADD EMPLOYES RULES]", e)

    # return vacancy_sheet_url & candidate_sheet_url

    return vacancy_url, candidate_url


