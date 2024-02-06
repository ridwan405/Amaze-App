from cryptography.fernet import Fernet
import os

class Encryptor():

    def create_key(self):
        key = Fernet.generate_key()
        return key

    def store_key_local(self, key, key_name):
        with open(key_name, 'wb') as user_key:
            user_key.write(key)

    def load_key(self, key_name):
        with open(key_name, 'rb') as user_key:
            key = user_key.read()
        return key

    def encrypt_file_name(self, key, file_name)-> str:

        f = Fernet(key)

        encrypted = f.encrypt(file_name.encode())

        return encrypted

    def decrypt_file_name(self, key, file_name)-> str:

        f = Fernet(key)

        decrypted = f.decrypt(file_name).decode()

        return decrypted

    def file_encrypt_local(self, key, original_file, encrypted_file):

        f = Fernet(key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open(encrypted_file, 'wb') as file:
            file.write(encrypted)

    def file_decrypt_local(self, key, encrypted_file, decrypted_file):

        f = Fernet(key)

        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()

        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, 'wb') as file:
            file.write(decrypted)


# test

# print(os.getcwd())
# encryptor=Encryptor()

# mykey=encryptor.create_key()

# encryptor.store_key_local(mykey, 'mykey.key')

# loaded_key=encryptor.load_key('mykey.key')

# enc_ = (encryptor.encrypt_file_name(loaded_key, 'CSE 299 project plan.pdf'))
# print(enc_)

# dec_ = (encryptor.decrypt_file_name(loaded_key, enc_))
# print(dec_)
# encryptor.file_encrypt_local(loaded_key, 'CSE 299 project plan.pdf', 'enc_')

# encryptor.file_decrypt_local(loaded_key, 'enc_', 'dec_CSE 299 project plan.pdf')
