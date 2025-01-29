from sheets.services.google.auth import spreadsheet_service

def add_rules_to_sheet(spreadsheet_id, sheet_name, range_string, allow_values):
    requests = []
    requests.append({
        'setDataValidation': {
            'range': {
                'sheetId': sheet_name,
                'startColumnIndex': 2,
                'endColumnIndex': 3
            },
            'rule': {
                'condition': {
                    'type': 'ONE_OF_LIST',
                    'values': allow_values
                },
                'inputMessage': 'Select from the list',
                'strict': True
            }
        }
    })