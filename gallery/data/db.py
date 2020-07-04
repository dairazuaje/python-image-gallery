import os
import psycopg2
import json
from psycopg2 import OperationalError, errorcodes, errors
from ..aws.secrets import *
from ..aws.s3 import *

# Configuration
# db_host = "module5-image-gallery.cyoqs8hmumyv.us-east-1.rds.amazonaws.com"
# db_name = "image_gallery"
# db_user = "image_gallery"
# password_file = "/home/ec2-user/.image_gallery_config"
# password = "Keldailin120217!"
BUCKET_NAME = "edu.au.cc.image-gallery-photos-dza0042"
# SQL Queries
sql_select_all = "SELECT * FROM users;"
sql_add = "INSERT INTO users VALUES (%s, %s, %s);"
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

# Retrieves password in original VPC that was created
#def get_secret():
#    jsonString = get_secret_image_gallery()
#   return json.loads(jsonString)


def get_password(secret):
    #return secret["password"]
    return os.getenv("IG_PASSWD")


def get_host(secret):
    #return secret["host_name"]
    return os.getenv("PG_HOST")


def get_username(secret):
    #return secret["username"]
    return os.getenv("IG_USER")

def get_database(secret):
    #return secret["database_name"]
    return os.getenv("IG_DATABASE")


def connect():
    global connection
    secret = get_secret()
    try:
        # connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = password)
        connection = psycopg2.connect(host=get_host(secret), dbname=get_database(secret), user=get_username(secret),
                                      password=get_password(secret))
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


def add(user, pw, fn):
    connect()
    global connection
    global cursor

    cursor = connection.cursor()

    cursor.execute(sql_add, (user, pw, fn,))
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
        print(error)


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

def close():
    connection.commit()
    cursor.close()
    connection.close()
