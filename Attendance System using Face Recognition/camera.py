# cap = cv2.VideoCapture(0)

# while True:

#     ret,frame = cap.read()
#     # img = cv2.resize(img,(360,360))
#     img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

#     face = face_recognition.face_locations(img)

#     cv2.rectangle(img,(face[3],face[0]),(face[1],face[2]),(255,0,0),2)

#     cv2.imshow('image',img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

def cam():
    
    import cv2
    import face_recognition

    cap = cv2.VideoCapture(0)

    while True:
        _, img = cap.read()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(img)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0,0,255), 2)

        # Display
        cv2.imshow('Webcam Check', img)

        # Stop if escape key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object
        
    cap.release()
    cv2.destroyAllWindows()