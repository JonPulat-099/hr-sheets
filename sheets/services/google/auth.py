from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os
from django.conf import settings


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


# TODO: Add try except block & handle exceptions
# try:
credentials = service_account.Credentials.from_service_account_file(
    os.path.join(settings.BASE_DIR, "credentials.json"), scopes=SCOPES
)

spreadsheet_service = build("sheets", "v4", credentials=credentials)
drive_service = build("drive", "v3", credentials=credentials)

# except Exception as e:
#     print(e)
#     spreadsheet_service = None
#     drive_service = None
