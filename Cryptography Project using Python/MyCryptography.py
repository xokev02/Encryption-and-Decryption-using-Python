# import required module
import db_helper
from cryptography.fernet import Fernet

import get_key


def decrypt_file(filename, user):
    global key

    try:
        key = db_helper.get_key_for_user(user)
    except Exception as e:
        print(e)
        exit()

    print("Key for " + user + ":" + key)

    fernet = Fernet(key)

    # opening the encrypted file
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = ''
    try:
        decrypted = fernet.decrypt(encrypted)
    except:
        print("Invalid Key!!!")
        exit()

    # opening the file in write mode and
    # writing the decrypted data
    with open(filename + "_dec", 'wb') as dec_file:
        dec_file.write(decrypted)


def encrypt_file(filename, user):
    global key

    try:
        key = db_helper.get_key_for_user(user)
    except Exception as e:
        print(e)
        exit()

    print("Key for " + user + ":" + key)

    fernet = Fernet(key)

    # opening the encrypted file
    with open(filename, 'rb') as enc_file:
        original = enc_file.read()
    # encrypting the file
    encrypted = ""
    try:
        encrypted = fernet.encrypt(original)
    except:
        print('Invalid Key!!!')
        exit()

    # opening the file in write mode and
    # writing the encrypted data

    with open(filename + "_" + user + "_enc", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def encrypt_message(message: str, user: str, fromuser: str):
    global key

    try:
        key = db_helper.get_key_for_user(user)
    except Exception as e:
        print(e)
        exit()

    print("Key for " + user + ":" + key)

    fernet = Fernet(key)

    encrypted = ""
    try:
        encrypted = fernet.encrypt(message.encode())
    except:
        print('Invalid Key!!!')
        exit()

    # opening the file in write mode and
    # writing the decrypted data
    db_helper.add_message_for_user(encrypted, user, fromuser)


def decrypt_all_messages(user: str, include_old=0):
    global key

    try:
        key = db_helper.get_key_for_user(user)
    except Exception as e:
        print(e)
        exit()

    print("Key for " + user + ":" + key)

    fernet = Fernet(key)

    records = db_helper.get_messages_for_user(user, include_old)
    if records is None:
        print("No messages available for user: " + user)
        return

    for row in records:
        decrypted = ""
        try:
            rowVal: str = row[0]
            fromUser: str = row[1]
            receivedOn = row[2]
            decrypted = fernet.decrypt(rowVal.encode())
            print("#####################  MESSAGE START  #####################")
            print("From: " + fromUser)
            print("Received: " + receivedOn.strftime("%m/%d/%Y, %H:%M:%S"))
            print("Message: " + decrypted.decode())
            print("#####################  MESSAGE END  #####################")
            print("")
        except Exception as e:
           print(e)
           exit()
