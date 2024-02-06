from uuid import uuid4
from django.db import models
from django.conf import settings


class EncryptionUser(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='encryption_users')

    key = models.BinaryField()




class EncryptionUserImage(models.Model):
    def user_directory_path(instance, filename):
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
        return 'user_{0}/{1}'.format(instance.user.id, filename)

    image_owner = models.ForeignKey(
        EncryptionUser, on_delete=models.CASCADE, related_name='images')

    image = models.ImageField(upload_to= user_directory_path)

class Folder(models.Model):
    folder_owner = models.ForeignKey(
        EncryptionUser, on_delete=models.CASCADE, related_name='folders')
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, related_name='folders')


class File(models.Model):
    # uid = models.UUIDField(primary_key=True, default=uuid4)
    uid = models.CharField(max_length=255, primary_key=True)

    file_owner = models.ForeignKey(
        EncryptionUser, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, related_name='files')
