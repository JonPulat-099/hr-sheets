import os
from dotenv import load_dotenv
from sheets.services.google.auth import spreadsheet_service, drive_service
from sheets.services.google.add_permission import permission
from sheets.services.google.add_rules import (
    add_rules_to_vacancies_sheet,
    add_rule_to_candidate_sheet,
)


load_dotenv()


def create_spreadsheet():
    try:
        from sheets.models import Config

        spreadsheet_details = {
            "properties": {"title": f"{os.getenv('COMPANY_NAME')} HR Dashboard"},
            "sheets": [
                {
                    "properties": {"title": "vacancies_all"},
                    "data": [
                        {
                            "rowData": {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Название организации"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Название вакансии"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Детали вакансии"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": "Зарплата"},
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Кол-во вакансий"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": " Топ вакансия"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                ]
                            }
                        }
                    ],
                },
                {
                    "properties": {"title": "candidates_all"},
                    "data": [
                        {
                            "rowData": {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Полное имя кандидата"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Эл. почта кандидата"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": "Пол"},
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Гражданство"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": "Зарплата"},
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": "Статус"},
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Название вакансии"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Название организации"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                ]
                            }
                        }
                    ],
                },
                {
                    "properties": {"title": "employees_all"},
                    "data": [
                        {
                            "rowData": {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Название организации"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Кол-во сотрудников"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Кол-во сотрудников (мужского пола)"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Кол-во сотрудников (женского пола)"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Всего экспатриантов"
                                        },
                                        "userEnteredFormat": {
                                            "textFormat": {"bold": True},
                                            "backgroundColorStyle": {
                                                "rgbColor": {
                                                    "red": 0.6,
                                                    "green": 0.6,
                                                    "blue": 0.6,
                                                }
                                            },
                                        },
                                    },
                                ]
                            }
                        }
                    ],
                },
            ],
        }

        sheet = (
            spreadsheet_service.spreadsheets()
            .create(body=spreadsheet_details, fields="spreadsheetId")
            .execute()
        )
        sheet_id = sheet.get("spreadsheetId")

        permission = {
            "type": "user",
            "role": "writer",
            "emailAddress": os.getenv("EMAIL") or "rjpm023@gmail.com",
        }

        # create file in drive with premissions
        file = (
            drive_service.permissions()
            .create(fileId=sheet_id, body=permission)
            .execute()
        )

        file_id = file.get("id")

        # write data to Config model
        Config.objects.create(key="company_name", value=os.getenv("COMPANY_NAME"))
        Config.objects.create(key="email", value=os.getenv("EMAIL"))
        Config.objects.create(
            key="sheet_url", value=f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        )
        Config.objects.create(key="sheet_id", value=sheet_id)
        Config.objects.create(key="file_id", value=file_id)

        return True
    except Exception as e:
        print(e)
        return False


def create_spreadsheet_organization(organization):
    spreadsheet_details = {
        "properties": {"title": f"{organization.name} HR Dashboard"},
        "sheets": [
            {
                "properties": {"title": "vacancies_all"},
                "data": [
                    {
                        "rowData": [
                            {
                                "values": [
                                    [
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Название организации"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {"bold": True},
                                                "backgroundColorStyle": {
                                                    "rgbColor": {
                                                        "red": 0.6,
                                                        "green": 0.6,
                                                        "blue": 0.6,
                                                    }
                                                },
                                            },
                                        },
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Название вакансии"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {"bold": True},
                                                "backgroundColorStyle": {
                                                    "rgbColor": {
                                                        "red": 0.6,
                                                        "green": 0.6,
                                                        "blue": 0.6,
                                                    }
                                                },
                                            },
                                        },
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Детали вакансии"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {"bold": True},
                                                "backgroundColorStyle": {
                                                    "rgbColor": {
                                                        "red": 0.6,
                                                        "green": 0.6,
                                                        "blue": 0.6,
                                                    }
                                                },
                                            },
                                        },
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Зарплата"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {"bold": True},
                                                "backgroundColorStyle": {
                                                    "rgbColor": {
                                                        "red": 0.6,
                                                        "green": 0.6,
                                                        "blue": 0.6,
                                                    }
                                                },
                                            },
                                        },
                                        {
                                            "userEnteredValue": {
                                                "stringValue": "Кол-во вакансий"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {"bold": True},
                                                "backgroundColorStyle": {
                                                    "rgbColor": {
                                                        "red": 0.6,
                                                        "green": 0.6,
                                                        "blue": 0.6,
                                                    }
                                                },
                                            },
                                        },
                                        {
                                            "userEnteredValue": {
                                                "stringValue": " Топ вакансия"
                                            },
                                            "userEnteredFormat": {
                                                "textFormat": {"bold": True},
                                                "backgroundColorStyle": {
                                                    "rgbColor": {
                                                        "red": 0.6,
                                                        "green": 0.6,
                                                        "blue": 0.6,
                                                    }
                                                },
                                            },
                                        },
                                    ],
                                ]
                            },
                            {
                                "values": [
                                    {
                                        "userEnteredValue": {
                                            "stringValue": f"{organization.name} [{organization.org_code}]"
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Тест вакансия"
                                        },
                                    },
                                    {
                                        "userEnteredValue": {
                                            "stringValue": "Подробности тестовой вакансии"
                                        },
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": "100000"},
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": "2"},
                                    },
                                    {
                                        "userEnteredValue": {"stringValue": "Да"},
                                    },
                                ],
                            },
                        ]
                    },
                ],
            },
            {
                "properties": {"title": "candidates_all"},
                "data": [
                    {
                        "rowData": {
                            "values": [
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Полное имя кандидата"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Эл. почта кандидата"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {"stringValue": "Пол"},
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {"stringValue": "Гражданство"},
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {"stringValue": "Зарплата"},
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {"stringValue": "Статус"},
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Название вакансии"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Название организации"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                            ]
                        }
                    }
                ],
            },
            {
                "properties": {"title": "employees_all"},
                "data": [
                    {
                        "rowData": {
                            "values": [
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Название организации"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Кол-во сотрудников"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Кол-во сотрудников (мужского пола)"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Кол-во сотрудников (женского пола)"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                                {
                                    "userEnteredValue": {
                                        "stringValue": "Всего экспатриантов"
                                    },
                                    "userEnteredFormat": {
                                        "textFormat": {"bold": True},
                                        "backgroundColorStyle": {
                                            "rgbColor": {
                                                "red": 0.6,
                                                "green": 0.6,
                                                "blue": 0.6,
                                            }
                                        },
                                    },
                                },
                            ]
                        }
                    }
                ],
            },
        ],
    }

    try:
        # create spreadsheet
        spreadsheet = (
            spreadsheet_service.spreadsheets()
            .create(body=spreadsheet_details, fields="spreadsheetId,sheets")
            .execute()
        )

        spreadsheet_id = spreadsheet.get("spreadsheetId")

        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}"

        emails = [os.getenv("EMAIL") or "rjpm023@gmail.com", organization.email]

        # add permissions
        for email in emails:
            try:
                permission(email, spreadsheet_id)
            except Exception as e:
                print("ERROR [PERMISSIONS] =>", e)

        # add rules
        sheets = spreadsheet.get('sheets', [])

        for sheet in sheets:
            sheet_id = sheet["properties"]["sheetId"]
            try:
                if sheet["properties"]["title"] == "vacancies_all":
                    add_rules_to_vacancies_sheet(
                        spreadsheet_id, sheet_id, organization, True
                    )
                elif sheet["properties"]["title"] == "candidates_all":
                    add_rule_to_candidate_sheet(spreadsheet_id, sheet_id, organization)
                elif sheet["properties"]["title"] == "employees_all":
                    add_rules_to_vacancies_sheet(
                        spreadsheet_id, sheet_id, organization, False
                    )
            except Exception as e:
                print("ERROR [ADD RULES] =>", e)

    except Exception as e:
        print('ERROR [CREATE SPREADSHEET] =>', e)
        pass

    return sheet_url
