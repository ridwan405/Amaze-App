from django.urls import path, include
from . import views

from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name= "index" ),
    path('social-auth/',include('social_django.urls',namespace='social')),
    path('authenticate', views.camera_auth, name= 'camera_auth' ),
    path('homepage/authpdf', views.camera_auth_pdf, name= 'camera_auth' ),
    path('homepage/authenticate', views.camera_auth_pdf, name= 'camera_auth_pdf' ),
    #  path('', TemplateView.as_view(template_name="index.html")),
    #path('accounts/', include('allauth.urls')),
    path('homepage/logout', LogoutView.as_view()),
    path('drive-list/logout', LogoutView.as_view()),
    path('homepage/', views.homepage, name= "homepage"),
    path('drive-list/', views.drive_list_files, name= "drive_list"),
    path('drive/<str:id>', views.drive_decrypt_file, name= "drive_decrypt_file"),
    path('drive/download', views.drive_download_file, name= "drive_download_file"),
    path('drive/getFile', views.drive_get_file_data, name= "drive_get_file_data"),
    path('drive/upload', views.drive_upload_file, name= "drive_get_file_data"),     
    path('drive/encrypt', views.drive_encrypt_file, name= "drive_encrypt_file"),     
    path('drive/decrypt', views.drive_decrypt_file, name= "drive_decrypt_file"),     
    path('drive/upload_file_of_choice', views.drive_upload_file_of_choice, name= "drive_upload_file_of_choice"),     
    path('drive-list/drive/upload_file_of_choice', views.drive_upload_file_of_choice, name= "drive_upload_file_of_choice"),  
    path('homepage/drive/upload_file_of_choice', views.drive_upload_file_of_choice, name= "drive_upload_file_of_choice"),   
       
   
]
