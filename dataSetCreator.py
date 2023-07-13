import cv2
import numpy as np
import os
import sqlite3
#insert/update data to sqlite
def insertOrUpdate(ID,Name,Age,Gender):
    conn=sqlite3.connect('FaceBase.db')
    query= "SELECT * FROM People WHERE ID= " +str(ID)
    cursor=conn.execute(query)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if(isRecordExist==0):
        query= "INSERT INTO People(ID,Name,Age,Gender) Values( " + str(ID) + ",'" + str(Name) + "','" + str(Age) + "','" + str(Gender) + "')"
    else:
        query= "UPDATE People SET Name='" + str(Name) + "',Age='" + str(Age) + "',Gender='" + str(Gender) + "'WHERE ID=" + str(ID)
    conn.execute(query)
    conn.commit()
    conn.close()
ID=input('Enter your id: ')
Name=input('Enter your name: ')
Age=input('Enter your age: ')
Gender=input('Enter your gender: ')
insertOrUpdate(ID,Name,Age,Gender)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cam = cv2.VideoCapture(0)
sampleNum=0
while(True):
    #camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
    #incrementing sample number
        sampleNum+=1
    #saving the captured face in the dataset folder
        cv2.imwrite('dataSet/User.'+str(ID) +'.'+ str(sampleNum) + '.jpg', gray[y:y+h,x:x+w])
        cv2.imshow('frame',img)
        cv2.waitKey(1)
    # break if the sample number is morethan 200
    if sampleNum>200:
        break
cam.release()
cv2.destroyAllWindows()
