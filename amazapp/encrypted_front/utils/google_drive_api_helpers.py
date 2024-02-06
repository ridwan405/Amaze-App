

# # got this from drive documentaion, slightly modified
# # used to access drive and and store access token

# from __future__ import print_function

# import os.path
# import io
# from pathlib import Path
# import time

# import base64

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
# from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# from cryptography.fernet import Fernet

# BASE_DIR = Path(__file__).resolve().parent.parent

# ENCRYPTED_FILE_PREFIX = 'encrypted_'

# # If modifying these scopes, delete the file token.json.
# SCOPES = [
#     'https://www.googleapis.com/auth/drive.metadata.readonly',
#     'https://www.googleapis.com/auth/drive.file',
#     'https://www.googleapis.com/auth/drive.readonly'
# ]


# """Shows basic usage of the Drive v3 API.
#     Prints the names and ids of the first 10 files the user has access to.
#     """
# creds = None
# # The file token.json stores the user's access and refresh tokens, and is
# # created automatically when the authorization flow completes for the first
# # time.
# if os.path.exists('token.json'):
#     creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             'credentials.json', SCOPES)
#         creds = flow.run_local_server(port=65259)
#         # Save the credentials for the next run
#     with open('token.json', 'w') as token:
#         token.write(creds.to_json())

# try:
#     service = build('drive', 'v3', credentials=creds)


# except HttpError as error:
#     # TODO(developer) - Handle errors from drive API.
#     print(f'An error occurred: {error}')


# # Call the Drive v3 API with methods


# def getFile():

#     files = []
#     page_token = None
#     while True:
#         # pylint: disable=maybe-no-member
#         response = service.files().list(q="mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document' or mimeType= 'application/pdf'",
#                                         spaces='drive',
#                                         fields='nextPageToken, '
#                                         'files(name, id)',
#                                         pageToken=page_token).execute()
#         # for file in response.get('files', []):
#         # Process change
#         # print(F'Found file: {file.get("name")}, {file.get("id")}')
#         files.extend(response.get('files', []))
#         page_token = response.get('nextPageToken', None)
#         if page_token is None:
#             break

#     return files


# # returns a dictionary containing file name, id, type
# def getFileData(fileId):

#     response = service.files().get(fileId=fileId).execute()

#     file = {
#         'name': response.get('name'),
#         'type': response.get('mimeType'),
#         'id': response.get('id')
#     }

#     return file

# # has no use, ignore


# def createFolder():
#     service.files().create(body={
#         'name': 'string', 'mimeType': 'application/vnd.google-apps.folder'}).execute()

# # perma deletes files from directory, get file from getFileData() defined above


# def deleteFile(file):

#     file_id = file['id']
#     service.files().delete(fileId=file_id).execute()


# # get file arg from getFileData() defined above
# def downloadFile(file):

#     file_name = file['name']
#     file_id = file['id']

#     # creating a dummy file
#     path = BASE_DIR/'utils'/'temp'

#     fp = open(os.path.join(path, file_name), 'x')
#     fp.close()

#     # downloading file
#     request = service.files().get_media(fileId=file_id)
#     file = io.BytesIO()
#     downloader = MediaIoBaseDownload(file, request)
#     done = False
#     while done is False:
#         status, done = downloader.next_chunk()
#         print(F'Download {int(status.progress() * 100)}.')

#     file.seek(0)

#     with open(os.path.join(path, file_name), 'wb') as f:
#         f.write(file.read())
#         f.close()


# # get file from getFileData() defined above
# def uploadFile(file):

#     path = BASE_DIR/'utils'/'temp'
#     file_name = file['name']

#     deleteFile(file)  # delete function for google drive
#     print("ORIGINAL FILE DELETED FROM DRIVE")

#     media = MediaFileUpload(os.path.join(path, file_name),
#                             mimetype=file['type'])

#     service.files().create(body={'name': file_name, 'mimeType': file['type']},
#                            media_body=media,
#                            fields='id').execute()

#     print("DONE UPLOAD")
#     media = None  # close media file, else conflicts


# def encryptFile(file, key):

#     downloadFile(file)

#     path = BASE_DIR/'utils'/'temp'

#     file_name = file['name']

#     # key = base64.urlsafe_b64encode(key)
#     print("ENCRYPTING-----------")
#     fernet = Fernet(key)

#     with open(os.path.join(path, file_name), 'rb') as F:
#         prepared_file = F.read()

#     encrypted = fernet.encrypt(prepared_file)

#     encrypted_file_name = ENCRYPTED_FILE_PREFIX + file_name

#     with open(os.path.join(path, encrypted_file_name), 'wb') as F:
#         F.write(encrypted)
#         F.close()

#     print("DONE ENRYPTING")

#     os.remove(os.path.join(path, file_name))
#     print("DELETED ORIGINAL FILE")

#     os.rename(os.path.join(path, encrypted_file_name),
#               os.path.join(path, file_name))

#     print("UPLOADING.............")
#     uploadFile(file)

#     os.remove(os.path.join(path, file_name))
#     print("DELETED LOCAL ENR FILE")


# def decryptFile(file, key):

#     downloadFile(file)

#     path = BASE_DIR/'utils'/'temp'

#     file_name = file['name']
#     with open(os.path.join(path, file_name), 'rb') as F:
#         prepared_file = F.read()

#     fernet = Fernet(key)
#     decrypted = fernet.decrypt(prepared_file)

#     decrypted_file_name = 'dec_' + file_name
#     with open(os.path.join(path, decrypted_file_name), 'wb') as F:
#         F.write(decrypted)
#         F.close()

#     print("DONE DECRYPTING")

#     os.remove(os.path.join(path, file_name))
#     print("DELETED LOCAL FILE")

#     os.rename(os.path.join(path, decrypted_file_name),
#               os.path.join(path, file_name))
#     print("UPLOADING.............")

#     uploadFile(file)

#     os.remove(os.path.join(path, file_name))
#     print("DELETED LOCAL DEC FILE")
