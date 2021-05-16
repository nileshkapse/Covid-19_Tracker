import mysql.connector
import uuid

cnx = mysql.connector.connect(user="root",password="password",host="localhost",database="root")

cursor = cnx.cursor(buffered=True)


username = input("Enter Username: ")
password = input("Enter Password: ")

query = ("INSERT INTO authUser VALUES(\""+ str(uuid.uuid4()) +"\",\"" + username + "\",\""+ password +"\");")
cursor.execute(query)

cnx.commit()

username = input("Enter Username: ")
password = input("Enter Password: ")

query = ("SELECT * from authUser where username=\""+ username +"\" and userpassword=\""+ password +"\";")

cursor.execute(query) 
list1 = cursor.fetchall()

print(list1)
if (len(list1) == 0):
  print("Unauthorized user")
else:
  print("Authorized user")    


cursor.close()
cnx.close()