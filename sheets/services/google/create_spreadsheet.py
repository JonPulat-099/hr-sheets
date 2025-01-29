import os
from dotenv import load_dotenv
from sheets.services.google.auth import spreadsheet_service, drive_service
from sheets.models import Config


load_dotenv()


def create_spreadsheet():
    try:
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
                                            "stringValue": "OrganizationName"
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
                                            "stringValue": "OrganizationCode"
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
                                            "stringValue": "OrganizationCategory"
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
                                            "stringValue": "VacancyName"
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
                                            "stringValue": "VacancyDetails"
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
                                            "stringValue": "VacancySalary"
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
                                            "stringValue": "VacancyCount"
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
                                            "stringValue": "CandidateName"
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
                                            "stringValue": "CandidateEmail"
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
                                            "stringValue": "CandidateGender"
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
                                            "stringValue": "CandidateCitizenship"
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
                                            "stringValue": "CandidateSalary"
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
                                            "stringValue": "CandidateState"
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
                                            "stringValue": "OrganizationName"
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
                                            "stringValue": "OrganizationCode"
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
