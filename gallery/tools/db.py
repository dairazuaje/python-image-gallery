import psycopg2
db_host = "demo-database-1.cyoqs8hmumyv.us-east-1.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

connection = None

password_file = "/home/ec2-user/.image_gallery_config"

def get_password():
    f = open(password_file, "r")
    result = f.readline()
    f.close()
    return result[:-1]

def connect():
    global connection
    connection = psycopg2.connect(host = db_host, dbname = db_name, user = db_user, password = get_password())
    
def execute(query, args = None):
    global connection
    cursor = connection.cursor()
    if not args:
        cursor.execute(query)
    else:
        cursor.execute(query, args)
    return cursor

def main():
    connect()
    res = execute("SELECT * FROM users;")
    for row in res:
        print(row)

    res = execute("UPDATE users SET password = %s WHERE username = 'dza0042';", ("Lincoln120217",))
    res = execute("SELECT * FROM users;")
    for row in res:
        print(row)
if __name__ == "__main__":
    main()
