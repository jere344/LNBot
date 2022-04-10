from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

GoogleAuth.DEFAULT_SETTINGS[
    "client_config_file"
] = "filesharing/google/client_secrets.json"

gauth = GoogleAuth()
gauth.LoadCredentialsFile("filesharing/google/mycreds.json")

if not gauth.credentials:
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile("filesharing/google/mycreds.json")

drive = GoogleDrive(gauth)


def upload_file(file_path, folder_names: tuple):
    parent_id = "root"
    for folder in folder_names:
        found = False
        for file in drive.ListFile(
            {
                "q": f"""title='{folder}' and mimeType='application/vnd.google-apps.folder' and trashed=false and '{parent_id}' in parents""",
            }
        ).GetList():
            parent_id = file["id"]
            found = True
            break
        if not found:
            file = drive.CreateFile(
                {
                    "title": folder,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [{"id": parent_id}],
                }
            )
            file.Upload()
            parent_id = file["id"]
            print(file["id"])

    file = drive.CreateFile({"parents": [{"id": parent_id}]})
    file.SetContentFile(file_path)
    file.Upload()

    return file
