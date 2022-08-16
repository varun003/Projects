## Entry Widget using Tkinter

from tkinter import *
import cv2
import os
import random
import csv
import face_recognition
import numpy as np
from datetime import datetime
from time import strftime
from csv import DictWriter




def attendance():
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    path = 'image_data'
    img = []
    classes = []
    images = os.listdir(path)

    for cl in images:
        im = cv2.imread(f'{path}/{cl}')
        img.append(im)
        classes.append(os.path.splitext(cl)[0])

    # print(classes)
    def encodings(img):
        encodeCollect = []
        for imgs in img:
            imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)
            # imgs = cv2.resize(imgs,(480,480))
            encode = face_recognition.face_encodings(imgs)[0]
            encodeCollect.append(encode)

        return encodeCollect

    encode_train = encodings(img)

    # print('encoding complete')

    cap = cv2.VideoCapture(0)

    while True:
        ret,img = cap.read()
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    
        face_locs = face_recognition.face_locations(img)
        face_encodes = face_recognition.face_encodings(img,face_locs)

        for faceLoc,faceEncode in zip(face_locs,face_encodes):
            match = face_recognition.compare_faces(encode_train,faceEncode)
            faceDist = face_recognition.face_distance(encode_train,faceEncode)

            # print(faceDist)

            # if the face distance between known face and unknown face is < 0.6,
            # it's a match else not matched,so we have to find the face with minimum distance

            matchMin = np.argmin(faceDist)

            if match[matchMin]:
                name = classes[matchMin]

                print('Name:',name,'Entry Time:',current_time)
                y1,x2,y2,x1 = faceLoc
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2,cv2.LINE_AA)
                cv2.rectangle(img,(x1,y2-30),(x2,y2),(255,0,0),cv2.FILLED)
                # cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,250,0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
                with open('attendance_data/timing.csv','a+') as f:
                    fieldnames = ['name','timing']
                    writer = csv.DictWriter(f,fieldnames=fieldnames) #

                    writer.writeheader()
                    writer.writerow({'name':name,'timing':current_time})

        cv2.imshow('webcam',img)


        if cv2.waitKey(4): #& 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def Read():
    with open('attendance_data/detail.csv','a+') as f:
        f.write(f"{namevalue.get()}\n")
        name = namevalue.get()
    cap = cv2.VideoCapture(0)

    while True:
        ret,frame = cap.read()
        
        cv2.imshow('image',frame)
        cv2.imwrite('image_data' + os.sep + name + '.jpg',frame)

        if cv2.waitKey(1):
            break
    cap.release()
    cv2.destroyAllWindows()



def New():
    global namevalue
    top1 = Toplevel()

    top1.geometry('500x500')
    top1.resizable(False,False)
    top1.title('Existing Employee Details')

    l1 = Label(top1,text='New Employee Registeration',font='comicsans 14 bold',padx=10).grid(row = 0,column=3,pady=50)

    name = Label(top1,text='Name',padx=20)
    # id = Label(top1,text='ID',padx=20)

    name.grid(row=1,column=2)
    # id.grid(row=2,column=2)

    namevalue = StringVar()
    # idvalue = StringVar()

    nameentry = Entry(top1,textvariable=namevalue).grid(row=1,column=3)
    # identry = Entry(top1,textvariable=idvalue).grid(row=2,column=3)

    Button(top1,text='Submit',command=Read).grid(row=4,column=3,pady=25)  # command

    top1.mainloop()

def Existing():
    top2 = Toplevel()

    top2.geometry('500x500')
    top2.resizable(False,False)
    top2.title('Existing Employee Details')

    l2 = Label(top2,text='Existing Employee Verification',font='comicsans 14 bold',padx=10).grid(row = 0,column=3,pady=50)
    
    name = Label(top2,text='Name',padx=20)
    # id = Label(top2,text='ID',padx=20)

    name.grid(row=1,column=2)
    # id.grid(row=2,column=2)

    namevalue = StringVar()
    # idvalue = StringVar()

    nameentry = Entry(top2,textvariable=namevalue).grid(row=1,column=3)
    # identry = Entry(top2,textvariable=idvalue).grid(row=2,column=3)

    Button(top2,text='Submit',command=attendance).grid(row=4,column=3,pady=25)  # command

    top2.mainloop()


root =  Tk()
root.geometry('500x500')
root.resizable(False,False)
root.title('Main Window')

Label(root,text='Face Recognition Based Attendance System',font='comicsans 14 bold').grid(row=0,column=2,pady=50,padx=50)
b1 = Button(text='New Employee',bg='black',fg='red',font= 'comicsansms 12 bold',command=New).grid(row = 10,column=2,pady=50)  
b2 = Button(text='Existing Employee',bg='black',fg='red',font= 'comicsansms 12 bold',command=Existing).grid(row = 11,column=2,pady=50)



root.mainloop()