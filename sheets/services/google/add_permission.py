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
    file = drive_service.permissions().create(
        fileId=file_id, body=permission).execute()
    return file


def update_permission(old_email, new_email, sheet_url):
    if sheet_url is None or old_email is None or new_email is None:
        return

    file_id = sheet_url.split("/")[-1]

    result = delete_persmission(sheet_url, old_email)

    if result:
        permission(new_email, file_id)
        return True

    return False


def delete_persmission(sheet_url, email):
    if sheet_url is None or email is None:
        return

    file_id = sheet_url.split("/")[-1]

    # list permissions
    permissions = (
        drive_service.permissions()
        .list(fileId=file_id, fields="permissions(id, type, role, emailAddress)")
        .execute()
    )

    permission_id = None

    for permission in permissions.get("permissions", []):
        if "emailAddress" in permission and permission["emailAddress"] == email:
            permission_id = permission["id"]
            break

    if permission_id is None:
        return False

    # delete permission
    drive_service.permissions().delete(
        fileId=file_id, permissionId=permission_id
    ).execute()

    return True
