import cv2
import numpy as np
import face_recognition


video_capture = cv2.VideoCapture(0)

# path = 'images'

burry_image = face_recognition.load_image_file('images/burry.jpg')
burry_encoding = face_recognition.face_encodings(burry_image)[0]

elon_image = face_recognition.load_image_file('images/burry.jpg')
elon_encoding = face_recognition.face_encodings(burry_image)[0]

known_face_encodings = [burry_encoding,elon_encoding]
known_face_names = ["burry","elon"]

while True:
    ret,frame = video_capture.read()

    # img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    rgb_frame = frame[:, :, ::-1]

    # find all the faces and face encodings in the frame of video

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame,face_locations)

    # loop through each face in this frame of video

    for (top,right,bottom,left),face_encodings in zip(face_locations,face_encodings):

        matches = face_recognition.compare_faces(known_face_encodings,face_encodings)

        name = 'unknown'

        face_distance = face_recognition.face_distance(known_face_encodings,face_encodings)
        best_match_index = np.argmin(face_distance)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]


        # drawing BB around face
        cv2.rectangle(frame,(left,top),(right,bottom),(0,0,255),2)

        # labeling name below face
        cv2.rectangle(frame,(left,bottom - 35),(right,bottom),(0,0,255),cv2.FILLED)
        cv2.rectangle(frame,name,(left+6,bottom-6),cv2.FONT_HERSHEY_DUPLEX,1.0,(255,255,255),1)

    cv2.imshow('video',frame)

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

    video_capture.release()
    cv2.destroyAllWindows()



