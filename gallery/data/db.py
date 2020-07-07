import os
import psycopg2
import json
import base64
from psycopg2 import OperationalError, errorcodes, errors
from PIL import Image
from ..aws.secrets import *
from ..aws.s3 import *


BUCKET_NAME = os.getenv("S3_IMAGE_BUCKET")
# SQL Queries
sql_select_all = "SELECT * FROM users;"
sql_add = "INSERT INTO users VALUES (%s, %s, %s, %s);"
sql_update_pw = "UPDATE users SET password = %s WHERE username = %s;"
sql_update_fn = "UPDATE users SET full_name = %s WHERE username = %s;"
sql_update_pw_fn = "UPDATE users SET full_name = %s, password = %s  WHERE username = %s;"
sql_delete = "DELETE FROM users WHERE username = %s;"
sql_columns = "SELECT * FROM users LIMIT 0"


# Gets password from secrets manager for RDS in ansible created VPC
# Modified some because secrets manager could not store secret properly using ansible varible
# def get_secret():
#    jsonString = get_secret_image_gallery()
#    jsonString = jsonString.replace("'", "\"")
#    sec = json.loads(jsonString)
#    return sec


def get_password():
    #return secret["password"]
    if os.getenv("IG_PASSWD_FILE") == None:
        print(os.getenv("IG_PASSWD"))
        return str(os.getenv("IG_PASSWD"))
    return str(os.getenv("IG_PASSWD_FILE"))
    

def get_host():
    #return secret["host_name"]
    print(os.getenv("PG_HOST"))
    return str(os.getenv("PG_HOST"))


def get_username():
    #return secret["username"]
    print(os.getenv("IG_USER"))
    return str(os.getenv("IG_USER"))

def get_database():
    #return secret["database_name"]
    print(os.getenv("IG_DATABASE"))
    return str(os.getenv("IG_DATABASE"))


def connect():
    global connection
    #secret = get_secret()
    try:
        # connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = password)
        connection = psycopg2.connect(host=get_host(), dbname=get_database(), user=get_username(), password=get_password())
    except psycopg2.DatabaseError as error:
        print(error)


def select_all():
    connect()
    global connection
    global cursor

    cursor = connection.cursor()
    cursor.execute(sql_select_all)
    result = cursor.fetchall()
    return result


def delete(user):
    connect()
    global connection
    global cursor

    cursor = connection.cursor()
    if check_user(user):
        cursor.execute(sql_delete, (user,))
        if cursor.rowcount == 1:
            print("User has been deleted")
    else:
        print("No such user.")

    close()


def add(user, pw, fn, user_type):
    connect()
    global connection
    global cursor

    cursor = connection.cursor()

    cursor.execute(sql_add, (user, pw, fn, user_type,))
    print("user added")
    if cursor.rowcount != -1:
        print("User has been added")
    else:
        print("Error: User not added")
    close()


def edit(user, pw, fn):
    connect()
    global connection
    global cursor

    cursor = connection.cursor()

    if check_user(user):
        if pw == "" and fn != "":
            cursor.execute(sql_update_fn, (fn, user,))
        elif fn == "" and pw != "":
            cursor.execute(sql_update_pw, (pw, user,))
        elif fn != "" or pw != "":
            cursor.execute(sql_update_pw_fn, (fn, pw, user,))

        if cursor.rowcount != -1:
            print("User has been edited")
        else:
            print("Error: User not updated")
    else:
        print("No such user.")

    close()


def check_user(user):
    cursor = connection.cursor()
    sql = "SELECT * FROM users WHERE username = %s;"
    cursor.execute(sql, (user,))
    if cursor.rowcount > 0:
        return True
    else:
        return False


def check_user_login(user):
    connect()
    global connection
    global cursor
    cursor = connection.cursor()
    sql = "SELECT user_type FROM users WHERE username = %s;"
    cursor.execute(sql, (user,))
    result = cursor.fetchall()
    print("Checking user: " + str(result[0][0]))
    if (result[0][0] == "User"):
        return True
    return False

def check_admin_login(user):
    connect()
    global connection
    global cursor
    cursor = connection.cursor()
    sql = "SELECT user_type FROM users WHERE username = %s;"
    cursor.execute(sql, (user,))
    result = cursor.fetchall()
    print("Checking admin: " + str(result[0][0]))
    if (result[0][0] == "Admin"):
        return True
    return False


def check_password(user, password):
    connect()
    global connection
    global cursor
    cursor = connection.cursor()
    sql = "SELECT full_name FROM users WHERE username = %s AND password = %s;"
    cursor.execute(sql, (user, password,))
    if cursor.rowcount > 0:
        return True
    else:
        return False


def add_image_db(username, filename):
    connect()
    global connection
    global cursor
    cursor = connection.cursor()
    sql = "INSERT INTO images (image_name, owner) VALUES (%s, %s);"
    cursor.execute(sql, (filename, username,))
    print("added!")
    close()


def get_images(username):
    connect()
    global connection
    global cursor
    cursor = connection.cursor()
    sql = "SELECT image_name FROM images WHERE owner =%s;"
    cursor.execute(sql, (username,))
    image_names = cursor.fetchall()
    images_arr = []
    directory = username + "/"

    for name in image_names:

        image_data = get_object(BUCKET_NAME, str(directory + name[0]))["Body"].read()
        image_b64 = base64.b64encode(image_data).decode("utf-8")

        image = {
            "name": name[0],
            "image": image_b64,
            "owner": username
        }

        images_arr.append(image)

    return images_arr

def delete_image(image_name, user):
    connect()
    global connection
    global cursor
    cursor = connection.cursor()
    sql = "DELETE FROM images WHERE image_name = %s AND owner = %s;"
    cursor.execute(sql, (image_name, user,))
    print("Image has been deleted")
    print("Image Name: " + image_name)
    print("Owner: " + user)
    close()

def close():
    connection.commit()
    cursor.close()
    connection.close()