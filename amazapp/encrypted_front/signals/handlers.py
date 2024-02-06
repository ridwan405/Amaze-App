from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from encrypted_front.models import EncryptionUser

from encrypted_front.utils.encryptor import Encryptor

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_encryptionuser_for_new_user(sender, **kwargs):
  if kwargs['created']:
    encryptor = Encryptor()
    key = encryptor.create_key()
    EncryptionUser.objects.create(user=kwargs['instance'], key = key)