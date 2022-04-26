import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Bhlohass*76",
    auth_plugin='mysql_native_password',
    )

my_cursor = mydb.cursor()

my_cursor.execute('CREATE DATABASE IF NOT EXISTS our_users')

my_cursor.execute('SHOW DATABASES')
for db in my_cursor:
    print(db)

