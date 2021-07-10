import cv2
import numpy as np
import face_recognition

import cv2
import face_recognition

imgA = face_recognition.load_image_file('Images/A1.jfif')
imgA = cv2.cvtColor(imgA, cv2.COLOR_BGR2RGB)
imgT = face_recognition.load_image_file('Images/At.jfif')
imgT = cv2.cvtColor(imgT, cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgA)[0]
encodeI = face_recognition.face_encodings(imgA)[0]
cv2.rectangle(imgA, (faceLoc[3], faceLoc[0]), (faceLoc[1], faceLoc[2]), (255, 0, 255), 2)

faceLocTest = face_recognition.face_locations(imgT)[0]
encodeTest = face_recognition.face_encodings(imgT)[0]
cv2.rectangle(imgT, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]), (255, 0, 255), 2)

results = face_recognition.compare_faces([encodeI], encodeTest)
faceDis = face_recognition.face_distance([encodeI], encodeTest)
print(results, faceDis)
cv2.putText(imgT, f'{results} {round(faceDis[0], 2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)

cv2.imshow('IMAGE 1', imgA)
cv2.imshow('IMAGE Test', imgT)
cv2.waitKey(0)
