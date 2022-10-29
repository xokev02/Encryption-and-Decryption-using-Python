import mysql.connector
from fernet import Fernet


def is_valid_user(username):
    mydb = mysql.connector.connect(user='developer', password='K3vin@123',
                                   host='127.0.0.1',
                                   database='new_schema')

    mycursor = mydb.cursor()

    mycursor.execute("select count(1) from new_schema.users where userFName='" + username + "'")
    records = mycursor.fetchall()
    count = 0
    for row in records:
        count = int(row[0])
        if count == 0:
            mydb.close()
            raise Exception("User not available")
        else:
            return count


def add_message_for_user(message: bytes, username, fromuser):
    mydb = mysql.connector.connect(user='developer', password='K3vin@123',
                                   host='127.0.0.1',
                                   database='new_schema')
    mycursor = mydb.cursor()

    try:
        sql = "INSERT INTO `new_schema`.`messages` (`UserFName`, `Message`, `FromUser`) VALUES ('" + username + "', '" + message.decode() + "', '" + fromuser + "')"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
    except Exception as e:
        mydb.close()
        raise Exception(e)


def get_messages_for_user(username, include_old):
    if include_old == 0:
        print("Reading ALL messages for : " + username)
    else:
        print("Reading NEW messages for : " + username)
    mydb = mysql.connector.connect(user='developer', password='K3vin@123',
                                   host='127.0.0.1',
                                   database='new_schema')

    mycursor = mydb.cursor()

    sql = ""
    if include_old == 0:
        sql = "select Message, FromUser, Received from new_schema.messages where userFName='" + username + "'"
    else:
        sql = "select Message, FromUser, Received from new_schema.messages where userFName='" + username + "' and Status=0"
    mycursor.execute(sql)
    records = mycursor.fetchall()

    sql = "update new_schema.messages set Status=1 where userFName='" + username + "'"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

    return records


def get_key_for_user(username):
    global key
    try:
        is_valid_user(username)
    except Exception as e:
        raise Exception(e)

    mydb = mysql.connector.connect(user='developer', password='K3vin@123',
                                   host='127.0.0.1',
                                   database='new_schema')
    mycursor = mydb.cursor()

    mycursor.execute("SELECT EncKey FROM new_schema.users where userFName='" + username + "'")

    records = mycursor.fetchall()
    if len(records):
        for row in records:
            key = row[0]

    mydb.close()

    if key is None or len(key) == 0:
        key = Fernet.generate_key()

        mydb = mysql.connector.connect(user='developer', password='K3vin@123',
                                       host='127.0.0.1',
                                       database='new_schema')
        mycursor = mydb.cursor()

        sql = "UPDATE new_schema.users SET EncKey = '" + key.decode() + "' WHERE UserFName = '" + username + "'"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
        return key.decode()
    else:
        return key
