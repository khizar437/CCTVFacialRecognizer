import pymongo
from datetime import datetime
from bson.objectid import ObjectId
client = pymongo.MongoClient("mongodb+srv://admin:TsZNZ2OSnRNEKSi4@cluster0.06su0.mongodb.net/test")
mydb = client["AttendanceData"]
att = mydb["Attendance"]
name = "ghjgha"
flag=0
now = datetime.now()
dtString = now.strftime('%H:%M:%S')
y=ObjectId()
data = {"_id":y, "name": name, "time": dtString}
for x in att.find({},{"_id": y, "name": 1, "time":1 }):
      if x["name"] == name:
          print(y)
          flag = 1
if flag == 0:            #when collection is empty
      att.insert(data)