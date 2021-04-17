import mysql.connector
from datetime import date

mydb = mysql.connector.connect(host="localhost", user="root", password="Quarantine12$", database="money_makers")
print("mydb:", mydb)
mycursor=mydb.cursor()
print("MyCursor:", mycursor)
date_tdy=date.today()
print("date:", date_tdy)
            
# insert source and destination message ids relation in database
sql= "INSERT INTO match_set (src_id, src_channel, dst_id, dst_channel, date) VALUES (%s, %s, %s, %s, %s)"
val= (100, -9099999, 30, -9088888, date_tdy)
print("SQL:", sql, val)
mycursor.execute(sql, val)
mydb.commit()
if (mydb.is_connected()):
    mycursor.close()
    mydb.close()
    print("MySQL connection is closed")
