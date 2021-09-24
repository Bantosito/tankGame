import mysql.connector
import socket
from datetime import datetime

def establishConnection(score):
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    mydb = mysql.connector.connect(user='webclient', password='raspberry',
                              host='127.0.0.1',
                              database='tankgame') 
    #print(mydb.is_connected()) 
    mycursor = mydb.cursor()
    sql = "INSERT INTO tankGameScores (user,score, date) VALUES (%s, %s, %s)"
    val = (socket.gethostname(),score,formatted_date )
    mycursor.execute(sql, val)
    
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
2
