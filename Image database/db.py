import mysql.connector


mydb=mysql.connector.connect(host='localhost',user="root",passwd="",database="blogdb")

mycursor=mydb.cursor()

mycursor.execute("CREATE TABLE `Python_Employee` ( `id` INT NOT NULL , `name` TEXT NOT NULL , `photo` BLOB NOT NULL , `biodata` BLOB NOT NULL , PRIMARY KEY (`id`))")

