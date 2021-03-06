import numpy as np
import cv2
import face_recognition
import os
from datetime import date
import datetime, time

images = []
known_names = []
encodings = []
names_list = []

def face_recog(img):
    if not img.any():
        placeholder_img = cv2.imread('img/placeholder.jpg')
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 1.5
        message = "Webcam not detected"
        text_size = cv2.getTextSize(message, font, scale, 2)[0]
        text_x = (placeholder_img.shape[1] - text_size[0]) / 2
        text_y = (placeholder_img.shape[0] + text_size[1]) / 2
        cv2.putText(placeholder_img, message, (int(text_x), int(text_y)), font, scale, (255, 255, 255), 2)
        resized_img = cv2.resize(placeholder_img, (750, 525))
        return resized_img
    else:
        # Grab a frame of video
        cap_img = img

        # Finds all the faces and their encodings in the current frame of video
        cap_face_loc = face_recognition.face_locations(cap_img)
        cap_face_enc = face_recognition.face_encodings(cap_img, cap_face_loc)

        # i and j represent each single face encoding and face location
        for i,j in zip(cap_face_enc, cap_face_loc):
            comparison = face_recognition.compare_faces(encodings, i)
            distances = face_recognition.face_distance(encodings, i)
            #print(distance)

            smallest_distance = np.argmin(distances)
            top, right, bottom, left = j
            color = (255, 0, 0)
            color2 = (0, 0, 255)
            font = cv2.FONT_HERSHEY_PLAIN

            if comparison[smallest_distance]:
                student_name = names_list[smallest_distance].upper()
                for i in os.listdir('img/images'):
                    student_number = known_names[smallest_distance][1]

                #makes rectangle with the name on each located face
                cv2.rectangle(cap_img,(left,top),(right,bottom), color , cv2.LINE_4)
                cv2.putText(cap_img, student_name,(left+8, top -8), font , 1, color2, 2)
                takeAttendance(student_name,student_number)
                
        resized_img = cv2.resize(cap_img, (750, 525))
        return resized_img

def getImages(path):

    known_images = os.listdir(path)
    j = 0

    for i in known_images:
        img = cv2.imread(f'{path}/{i}')
        images.append(img)
        known_names.append(os.path.splitext(i)[0].split("_"))
        names_list.append(known_names[j][0])
        j+=1
        #print(names_list)
    return names_list

def getEncodings(images):

    encodedList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encoded = face_recognition.face_encodings(img)[0]
        encodedList.append(encoded)
    encodings = encodedList
    return encodedList

def takeAttendance(student_name,student_number):
    file = open('attendance_list.csv', 'r+')
    data = file.readlines()
    names = []
    for i in data:
        line_list = i.split(',')
        names.append(line_list[0])
   # if student_name not in names:
        x = datetime.datetime.now()
        file.writelines(f'\n{student_name},{student_number},{x.strftime("%a %b %d")},{x.strftime("%X")}')

#getImages('img/images')
#encodings = getEncodings(images)
#print('Encoding Complete!')
#face_recog()


