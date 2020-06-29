import psycopg2
import json
from psycopg2 import OperationalError, errorcodes, errors
from .secrets import *

# Configuration
#db_host = "module5-image-gallery.cyoqs8hmumyv.us-east-1.rds.amazonaws.com"
#db_name = "image_gallery"
#db_user = "image_gallery"
# password_file = "/home/ec2-user/.image_gallery_config"
#password = "Keldailin120217!"

# SQL Queries
sql_select_all = "SELECT * FROM users;"
sql_add = "INSERT INTO users VALUES (%s, %s, %s);"
sql_update_pw = "UPDATE users SET password = %s WHERE username = %s;"
sql_update_fn = "UPDATE users SET full_name = %s WHERE username = %s;"
sql_update_pw_fn = "UPDATE users SET full_name = %s, password = %s  WHERE username = %s;"
sql_delete = "DELETE FROM users WHERE username = %s;"
sql_columns = "SELECT * FROM users LIMIT 0"


def get_secret():
    jsonString = get_secret_M5()
    jsonString = json.dumps(jsonString)
    return json.loads(jsonString)


def get_password(secret):
    return secret["password"]


def get_host(secret):
    return secret["host"]


def get_username(secret):
    return secret["username"]


def get_database(secret):
    return secret["database_name"]


def connect():
    global connection
    secret = get_secret()
    try:
        #connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = password)
        connection = psycopg2.connect(host=get_host(secret), dbname=get_database(secret), user=get_username(secret), password=get_password(secret))
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
    print("I AM GETTING CALLED!")
    print(user)
    cursor = connection.cursor()
    sql = "SELECT * FROM users WHERE username = %s;"
    cursor.execute(sql, (user,))
    if cursor.rowcount > 0:
        print("YEP")
        return True
    else:
        print("NOPE")
        return False
        print(error)


def close():
    connection.commit()
    cursor.close()
    connection.close()

