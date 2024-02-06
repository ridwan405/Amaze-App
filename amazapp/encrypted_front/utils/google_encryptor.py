from .encryptor import Encryptor
from .google_drive_quickstart import *


class GoogleOAuth2Encryptor():


    encryptor=Encryptor()

    mykey=encryptor.create_key()

    # encryptor.store_key_local(mykey, 'mykey.key')

    loaded_key=encryptor.load_key('mykey.key')

    enc_ = (encryptor.encrypt_file_name(loaded_key, 'CSE 299 project plan.pdf'))
    print(enc_)

    dec_ = (encryptor.decrypt_file_name(loaded_key, enc_))
    print(dec_)
    encryptor.file_encrypt_local(loaded_key, 'CSE 299 project plan.pdf', 'enc_')

    encryptor.file_decrypt_local(loaded_key, 'enc_', 'dec_CSE 299 project plan.pdf')
    # def __init__(self, client_id, client_secret):