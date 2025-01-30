from sheets.services.google.auth import spreadsheet_service


def add_rules_to_sheet(spreadsheet_id, sheet_id):
    requests = []
    requests.append(
        {
            "setDataValidation": {
                "range": {
                    "sheetId": sheet_id,
                    "startColumnIndex": 2,
                    "endColumnIndex": 3,
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [
                            {
                                'userEnteredValue': 'male'
                            },
                            {
                                'userEnteredValue': 'female'
                            },
                        ],
                    },
                    "showCustomUi": True,
                    "inputMessage": "Select from the list",
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
