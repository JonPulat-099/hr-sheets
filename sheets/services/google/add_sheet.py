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
                "OrganizationName",
                "VacancyName",
                "VacancyDetails",
                "VacancySalary",
                "VacancyCount",
            ],
            [
                f"{organization.name} [{organization.org_code}]",
                "Тест вакансия",
                "Подробности тестовой вакансии",
                "100000",
                "1",
            ],
        ]
    }

    # candidate_sheet_header
    candidate_sheet_range_body = {
        "values": [
            [
                "CandidateName",
                "CandidateEmail",
                "CandidateGender",
                "CandidateCitizenship",
                "CandidateSalary",
                "CandidateState",
                "VacancyName",
                "OrganizationName",
            ],
        ]
    }

    # add headers to the new sheets
    spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheets[0]}!A1",
        valueInputOption="RAW",
        body=vacancy_sheet_range_body,
    ).execute()

    spreadsheet_service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheets[1]}!A1",
        valueInputOption="RAW",
        body=candidate_sheet_range_body,
    ).execute()

    add_rule_to_candidate_sheet(
        spreadsheet_id,
        new_sheets["replies"][1]["addSheet"]["properties"]["sheetId"],
        organization,
    )

    add_rules_to_vacancies_sheet(
        spreadsheet_id,
        new_sheets["replies"][0]["addSheet"]["properties"]["sheetId"],
        organization,
    )

    # return vacancy_sheet_url & candidate_sheet_url
    vacancy_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={
        new_sheets['replies'][0]['addSheet']['properties']['sheetId']}"
    candidate_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={
        new_sheets['replies'][1]['addSheet']['properties']['sheetId']}"

    return vacancy_url, candidate_url
