import datetime
import os
import cv2
import numpy as np
import csv
from RTAMS import *

#url = url of camera stream

# Attendance File Creation
now = datetime.datetime.now()
fileName = 'Attendance-' + now.strftime("%d%m%Y-%H%M%S") + '.csv'
with open(fileName, mode='w', newline='') as file:
    writer = csv.writer(file, dialect='excel')
    writer.writerow([]) 

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    data = [[name, now.strftime('%H:%M:%S')]]
    with open(fileName, mode='a', newline='') as file:
        writer = csv.writer(file, dialect='excel')
        writer.writerows(data)

def start():
   
    path =  r'src_imgs'
    images =[]
    classNames = []
    for item in os.listdir(path):
        curImg = cv2.imread(f'{path}/{item}')
        images.append(curImg)
        classNames.append(os.path.splitext(item)[0])
    names = []
    encodeListKnown = findEncodings(images)
    capture = cv2.VideoCapture('http://192.168.107.85:4747/video?640x480')
    while True:
        success, img = capture.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_locations(imgS)
        encodesCurFrame = face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = compare_faces(encodeListKnown, encodeFace)
            faceDis = face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                if name not in names:
                    names.append(name)
                    markAttendance(name)
        cv2.imshow('Webcam', img)
        key=cv2.waitKey(5)
        if key==ord('q'):
            break
    cv2.destroyAllWindows()
    cv2.imread
