import mysql.connector

mydb=mysql.connector.connect(host='localhost',user="user",passwd="",database="my")

mycursor=mydb.cursor()

id=10
mycursor.execute("SELECT * FROM articles WHERE id = %s", [id])

myresult=mycursor.fetchone()




# password=myresult[password]
print(myresult)