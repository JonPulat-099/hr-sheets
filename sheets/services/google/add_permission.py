from sheets.services.google.auth import drive_service


def permission(email, file_id):
    if email is None or file_id is None:
        return
    
    permission = {
        "type": "user",
        "role": "writer",
        "emailAddress": email,
    }

    # create file in drive with premissions
    file = drive_service.permissions().create(fileId=file_id, body=permission).execute()
