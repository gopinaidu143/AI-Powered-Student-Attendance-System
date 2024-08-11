import pickle
import face_recognition
import cv2
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("faceattendancerealtime-50d48-firebase-adminsdk-dqvrs-34b6851fed.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://faceattendancerealtime-50d48-default-rtdb.firebaseio.com/",
    'storageBucket': "faceattendancerealtime-50d48.appspot.com"
})


folderPath = 'Images'
modePathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in modePathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    # print(path)
    # print(os.path.splitext(path)[0])

def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)


    return encodeList

encodeListKnown = findEncoding(imgList)
encodeListKnownWithIDs = [encodeListKnown,studentIds]
file = open("encodeFile.p",'wb')
pickle.dump(encodeListKnownWithIDs,file)
file.close()
print("file saved")

