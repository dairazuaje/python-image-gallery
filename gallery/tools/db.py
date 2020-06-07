import psycopg2
from psycopg2 import OperationalError, errorcodes, errors

# Configuration
db_host = "demo-database-1.cyoqs8hmumyv.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"
password_file = "/home/ec2-user/.image_gallery_config"

# SQL Queries
sql_select_all = "SELECT * FROM users;"
sql_add = "INSERT INTO users VALUES (%s, %s, %s);"
sql_update_pw = "UPDATE users SET password = %s WHERE username = %s;"
sql_update_fn = "UPDATE users SET full_name = %s WHERE username = %s;"
sql_update_pw_fn = "UPDATE users SET full_name = %s, password = %s  WHERE username = %s;"
sql_delete = "DELETE FROM users WHERE username = %s;"
sql_columns = "SELECT * FROM users LIMIT 0"

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

def connect():
    global connection
    try:
        connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = get_password())
    except psycopg2.DatabaseError as error:
        print(error)

def select_all():
    global connection
    global cursor
    try:
        connection =  psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = get_password())
        cursor = connection.cursor()

        cursor.execute(sql_select_all)
        colnames = [desc[0] for desc in cursor.description] # Retrieves column names from database to then display with SELECT * results 
                
        for column in colnames:
            print("{: <25}".format(column.upper()), end = " ")

        print()
        result = cursor.fetchall()
        for row in result:
            print("{: <25} {: <25} {: <25}".format(*row))
            
    except psycopg2.DatabaseError as error:
        print(error)

    finally:
        if connection is not None:
            close()

def delete(user):
    global connection
    global cursor
    try:
        connection =  psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = get_password())
        cursor = connection.cursor()
        cursor.execute(sql_delete, (user,))

        if cursor.rowcount == 1:
            print("User has been deleted")
        elif cursor.rowcount == 0:
            print("No such user.")

    except psycopg2.DatabaseError as error:
        print(error)

    finally:
        if connection is not None:
            close()

def add(user, pw, fn):       
    global connection
    global cursor
    try:
        connection =  psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = get_password())
        cursor = connection.cursor()

        cursor.execute(sql_add, (user, pw, fn,))
        if cursor.rowcount != -1:
            print("User has been added")
        else: 
            print("Error: User not added")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            close()

def edit(user, pw, fn):              
    global connection
    global cursor
    try:
        connection =  psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = get_password())
        cursor = connection.cursor()
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

    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if connection is not None:
            close()
            
def close():
    connection.commit()
    cursor.close()
