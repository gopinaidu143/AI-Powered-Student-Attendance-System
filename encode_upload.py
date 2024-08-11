import pickle
import face_recognition
import cv2
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

def save_encodings_to_file(folderPath):

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

    def findEncoding(imagesList):
        encodeList = []
        for img in imagesList:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)

        print(encodeList)
        return encodeList

    encodeListKnown = findEncoding(imgList)
    encodeListKnownWithIDs = [encodeListKnown,studentIds]
    file = open("encodeFile.p",'wb')
    pickle.dump(encodeListKnownWithIDs,file)
    file.close()
    print("File saved")

# If you want to use this function in another file, you can simply import it and call it with the folderPath argument.
