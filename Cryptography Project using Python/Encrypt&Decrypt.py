# import required module
import mysql.connector
from cryptography.fernet import Fernet
import base64

import get_key

key = get_key.get_key_for_user('Jane')
print(key)

# key generation
# key = Fernet.generate_key()

# string the key in a file
#with open('filekey.key', 'wb') as filekey:
#    filekey.write(bytes(key))

# using the generated key
fernet = Fernet(key)

# opening the original file to encrypt
with open('Secret', 'rb') as file:
    original = file.read()

# encrypting the file                           Secret
encrypted = fernet.encrypt(original)

# opening the file in write mode and
# writing the encrypted data
with open('Secret1', 'wb') as encrypted_file:
    encrypted_file.write(encrypted)
# using the key
fernet = Fernet(key)

# opening the encrypted file
with open('Secret1', 'rb') as enc_file:
    encrypted = enc_file.read()

# decrypting the file
decrypted = fernet.decrypt(encrypted)

# opening the file in write mode and
# writing the decrypted data
with open('Secret2', 'wb') as dec_file:
    dec_file.write(decrypted)
