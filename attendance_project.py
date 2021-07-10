import cv2
import numpy as np
import face_recognition
import pymongo
import os
from datetime import datetime
from datetime import date
from bson.objectid import ObjectId

#mongo
client = pymongo.MongoClient("mongodb+srv://admin:TsZNZ2OSnRNEKSi4@cluster0.06su0.mongodb.net/test")    #connecting to client
mydb = client["AttendanceData"]     #database
att = mydb["Attendance"]  #collection

# from PIL import ImageGrab
path = 'C:/Users/kdkri/PycharmProjects/FacialRecognitionProject/ImagesAttendance'   #path to data-folder
images = []
clNames = []
myList = os.listdir(path)  #extracts name of imgs in database
#print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)  #list of images in myList
    clNames.append(os.path.splitext(cl)[0]) #print name without filetype
#print(clNames)

def findEncodings(images):  #to extract encodings of "images"
    enList = []
    for img in images:   #extract each img in images
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]  #extract encoding of (RGB)img
        enList.append(encode)  #added to enList
    return enList

#to update data in local csv file
#def markAttendance(name):
    #with open('data.csv','r+') as f:
     #   att.update_many()
      #  myDataList = f.readlines()
       # nameList = []
        #for line in myDataList:
         #   entry = line.split(',')
          #  nameList.append(entry[0])
    #    if name not in nameList:
     #       now = datetime.now()
      ##     f.writelines(f'\n{name},{dtString}')

#### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# def captureScreen(bbox=(300,300,690+300,530+300)):
#     capScr = np.array(ImageGrab.grab(bbox))
#     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
#     return capScr

#to update data into mongodb
def markAttendance(name):
  flag=0
  now = datetime.now()
  today = date.today()
  d = today.strftime("%d/%m/%Y")
  dtString = now.strftime('%H:%M:%S')
  y = ObjectId()     #create a new object id
  data = {"_id": y, "name": name, "date": d, "time": dtString}
  for x in att.find({}, {"name": 1,"date": 1, "time": 1}):
      if x["name"] == name :
         if x["date"]== d:
            flag=1
  if flag == 0:  # when collection is empty
      att.insert_one(data)



enListKnown = findEncodings(images)   #encoding of known imgs from database
print('Encoding Complete')

cap = cv2.VideoCapture(0)   #to extract the livestream from CCTV

while True:
    success, img = cap.read()  #extracting image frame-wise
    #img = captureScreen()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)  #resizing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB) #converting to rgb
        #extracting and encoding of each face detected within frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(enListKnown,encodeFace)
        faceDis = face_recognition.face_distance(enListKnown,encodeFace)
        #print(faceDis)
        matchIndex = np.argmin(faceDis)   #finds index of matching img

        if matches[matchIndex]:
            name = clNames[matchIndex].upper()
            #print(name)
            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
