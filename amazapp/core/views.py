
import json
import os.path
import urllib.request

from pathlib import Path
from shutil import copyfile

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from encrypted_front.utils import google_drive_quickstart, file_upload_handler 
from encrypted_front.models import EncryptionUser
from core.forms import UploadFileForm

import face_recognition
import spoof_check_api
import time


BASE_DIR = Path(__file__).resolve().parent.parent
SPOOF_CHECK_THRESHOLD_REAL = .60 # image has to be about 60% human like


def index(request):

    authenticated = False
    return render(request, 'index.html', {'authenticated': authenticated})


def logout(request):
    return render(request, 'index.html')

# for login
def camera_auth(request):
    if request.method == 'POST':

        path = request.POST['src']
        # print('data uri is :'+path)

        # print(urllib.request.urlopen(path))

        web_path = BASE_DIR
        db_path = BASE_DIR/'core'/'utils'/'db'

        file_name = str(request.user.id) + '.png'
        urllib.request.urlretrieve(path, file_name)
        # current_session_image_file = os.path.join(web_path, file_name)

        # spoof_check_result = json.loads(spoof_check_api.check_image_for_spoofing(
        #     current_session_image_file).text)
        # print(spoof_check_result['doc_json'])

        if os.path.exists(os.path.join(db_path, file_name)):
            authenticated= True
            # if float(spoof_check_result['doc_json']['real']) > SPOOF_CHECK_THRESHOLD_REAL:

            #     authenticated = face_recognition.imgVerify(os.path.join(
            #         web_path, file_name), current_session_image_file, True)
            #     os.remove(os.path.join(web_path, file_name))
            # else:
            #     authenticated = False
        else:
            # creating a dummy file

            fp = open(os.path.join(db_path, file_name), 'x')
            fp.close()

            src = os.path.join(web_path, file_name)
            dst = os.path.join(db_path, file_name)
            copyfile(src, dst)
            os.remove(os.path.join(web_path, file_name))
            authenticated = True

        return HttpResponseRedirect('/homepage/')
    else:
        authenticated = False
        return render(request, 'CameraApp.html', {'authenticated': authenticated})
    

    
def homepage(request):
    return render(request, 'home.html')


def drive_list_files(request):
    service = google_drive_quickstart.driveStart()
    items = google_drive_quickstart.getFile(service)
    # items = [{'name': 'target', 'id' :'11nxBpsR-bVcYY5JDGZ2ksnQWatb3tzwf'}]
    return render(request, 'drive.html', {'items': items})


def drive_get_file_data(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        service = google_drive_quickstart.driveStart()
        file = google_drive_quickstart.getFileData(service, file_id)
        print(file)
        return render(request, 'drive.html')
    else:
        return render(request, 'drive.html')


def drive_download_file(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        service = google_drive_quickstart.driveStart()
        file = google_drive_quickstart.getFileData(service, file_id)
        google_drive_quickstart.downloadFile(service, file)
        return render(request, 'drive.html')
    else:
        return (request, 'drive.html')


def drive_upload_file(request):
    if request.method == 'POST':
        file_id = request.POST['file_id']
        service = google_drive_quickstart.driveStart()
        file = google_drive_quickstart.getFileData(service, file_id)

        google_drive_quickstart.uploadFile(file)

        return render(request, 'drive.html')
    else:
        return render(request, 'drive.html')

def drive_upload_file_of_choice(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            service = google_drive_quickstart.driveStart()
            submitted_file = request.FILES['file']

            file_upload_handler.handle_uploaded_file(submitted_file)

            file_name = submitted_file.name
            file_type = submitted_file.content_type
            file_path = BASE_DIR/'encrypted_front'/'utils'/'temp'

            encryption_user = EncryptionUser.objects.get(user_id=request.user.id)
            key = encryption_user.key
            
            google_drive_quickstart.base_encryptFile(service, file_name, file_path, file_type, key)
            return HttpResponseRedirect('/homepage/')
    else:
        form = UploadFileForm()
        return render(request, 'upload_file.html', {'form': form})


def drive_encrypt_file(request):

    encryption_user = EncryptionUser.objects.get(user_id=request.user.id)
    key = encryption_user.key

    if request.method == 'POST':
        file_id = request.POST['file_id']
        service = google_drive_quickstart.driveStart()
        file = google_drive_quickstart.getFileData(service, file_id)

        google_drive_quickstart.encryptFile(service, file, key)

        return render(request, 'drive.html')
    else:
        return render(request, 'drive.html')
    
    
def pdf_view(file_data):
    
    path= file_data['path']
    name= file_data['name']
    
    with open(os.path.join(path, name), 'rb') as pdf:
        response = HttpResponse(pdf.read(),content_type='application/pdf')
        response['Content-Disposition'] = 'filename='+name
        pdf.closed
        
        os.remove(os.path.join(path, 'encrypted_'+name))
        print("DELETED LOCAL FILE")
        return response


def drive_decrypt_file(request, id):

    encryption_user = EncryptionUser.objects.get(user_id=request.user.id)
    key = encryption_user.key

    
    file_id = id
    
    service = google_drive_quickstart.driveStart()
    file = google_drive_quickstart.getFileData(service, file_id)

    file_data= google_drive_quickstart.decryptFile(service, file, key)
    

    return pdf_view(file_data)

# for pdf authentication   
def camera_auth_pdf(request):
    
    
   

    if request.method == 'POST':

        path = request.POST['src']
       

        web_path = BASE_DIR
        db_path = BASE_DIR/'core'/'utils'/'db'

        file_name = str(request.user.id) + '.png'
        urllib.request.urlretrieve(path, file_name)
        

        if os.path.exists(os.path.join(db_path, file_name)):
            
            # if float(spoof_check_result['doc_json']['real']) > SPOOF_CHECK_THRESHOLD_REAL:

            authenticated = face_recognition.imgVerify(file_name, file_name, True)
            os.remove(os.path.join(web_path, file_name))
            if(authenticated):
                return HttpResponseRedirect('/drive-list/')
            else:
                return HttpResponseRedirect ('/homepage/')
            # else:
            #     authenticated = False
        else:
            # creating a dummy file

            fp = open(os.path.join(db_path, file_name), 'x')
            fp.close()

            src = os.path.join(web_path, file_name)
            dst = os.path.join(db_path, file_name)
            copyfile(src, dst)
            os.remove(os.path.join(web_path, file_name))
            authenticated = True

        return HttpResponseRedirect('/homepage/')
    else:
        authenticated = False
        return render(request, 'CameraApp.html', {'authenticated': authenticated})
    
    # if request.method == 'POST':

    #     path = request.POST['src']
        

    #     web_path = BASE_DIR
    #     db_path = BASE_DIR/'core'/'utils'/'db'

    #     file_name = str(request.user.id) + '.png'
    #     urllib.request.urlretrieve(path, file_name)
        
        
    #     if os.path.exists(os.path.join(db_path, file_name)):
            
    #         authenticated = face_recognition.imgVerify(file_name,file_name, True)
    #         os.remove(os.path.join(web_path, file_name))
            
    #         if(authenticated):
    #             return drive_decrypt_file(request, id)
    #         else:
            
    #             return render(request, 'CameraApp.html', {'authenticated': authenticated})
    #     else:
    #         return HttpResponseRedirect('/index/')
    # else:
    #     return render(request, 'drive.html')
    
        
