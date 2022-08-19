import cv2
import mediapipe as mp
from tkinter import *
import math as m



def findAngle(x1, y1, x2, y2):
    theta = m.acos( (y2 -y1)*(-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
    degree = int(180/m.pi)*theta
    degree = degree - 90
    return degree


def face():
    mp_drawing = mp.solutions.drawing_utils
    mp_face_detection = mp.solutions.face_detection

    video = cv2.VideoCapture(0)

    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while True:
            ret, image = video.read()
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = face_detection.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)

            cv2.imshow('MediaPipe Face Detection', image)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break

    video.release()
    cv2.destroyAllWindows()
    return "Yeah! Face landmarks successfully detected :)"

def squat():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    video = cv2.VideoCapture('squat.mp4')

    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        while video.isOpened():
            success, image = video.read()
            # if not success:
            #     print("Ignoring empty camera frame.")
            #     continue
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # image.flags.writeable = False
            results = pose.process(image)
            # image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            lm = results.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            # landmarking coordinates

            right_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x * w)
            right_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y * h)

            right_knee_x = int(lm.landmark[lmPose.RIGHT_KNEE].x * w)
            right_knee_y = int(lm.landmark[lmPose.RIGHT_KNEE].y * h)

            right_ankle_x = int(lm.landmark[lmPose.RIGHT_ANKLE].x * w)
            right_ankle_y = int(lm.landmark[lmPose.RIGHT_ANKLE].y * h)  

        
            # finding Knee Inclination
            knee_inclination = findAngle(right_knee_x,right_knee_y,right_ankle_x,right_ankle_y)
            

            cv2.circle(image,(right_knee_x,right_knee_y),5,(0,255,0),-1)
            cv2.circle(image,(right_ankle_x,right_ankle_y),5,(0,255,0),-1)


            # joining landmarks
            # cv2.line(image,(right_shoulder_x,right_shoulder_y),(right_hip_x,right_hip_y),(0,255,255),4)

            cv2.line(image,(right_knee_x,right_knee_y),(right_ankle_x,right_ankle_y),(0,0,255),4)


            # displaying angle on hip

            # cv2.putText(image,str(int(torso_inclination)),(right_hip_x,right_hip_y),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)
            # cv2.putText(image,"Torso Inclination:"+str(int(torso_inclination)),(700,40),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),2)

            cv2.putText(image,str(int(knee_inclination)),(right_knee_x,right_knee_y),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),2)
            cv2.putText(image,"Neck Inclination:"+str(int(knee_inclination)),(700,80),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)

            
            # mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                    #   landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            cv2.imshow('MediaPipe Pose', image)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
    video.release()
    cv2.destroyAllWindows()
    return "Yeah! pose landmarks successfully detected :)"
    
def back():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    video = cv2.VideoCapture('video/body_posture.mp4')

    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
        while video.isOpened():
            success, image = video.read()
            # if not success:
            #     print("Ignoring empty camera frame.")
            #     continue
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # image.flags.writeable = False
            results = pose.process(image)
            # image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            lm = results.pose_landmarks
            lmPose = mp_pose.PoseLandmark

            # landmarking coordinates
            right_shoulder_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
            right_shoulder_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

            right_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x * w)
            right_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y * h)

            right_knee_x = int(lm.landmark[lmPose.RIGHT_KNEE].x * w)
            right_knee_y = int(lm.landmark[lmPose.RIGHT_KNEE].y * h)

            right_ear_x = int(lm.landmark[lmPose.RIGHT_EAR].x * w)
            right_ear_y = int(lm.landmark[lmPose.RIGHT_EAR].y * h)  

            # finding torso's inclination
            torso_inclination = findAngle(right_shoulder_x,right_shoulder_y,right_hip_x,right_hip_y)

            # finding Neck Inclination
            neck_inclination = findAngle(right_ear_x,right_ear_y,right_shoulder_x,right_shoulder_y)
            # lamdmarking torso and neck inclination
            cv2.circle(image,(right_shoulder_x,right_shoulder_y),5,(0,0,255),-1)
            cv2.circle(image,(right_hip_x,right_hip_y),5,(0,0,255),-1)

            cv2.circle(image,(right_ear_x,right_ear_y),5,(0,255,0),-1)
            cv2.circle(image,(right_shoulder_x,right_shoulder_y),5,(0,255,0),-1)


            # joining landmarks
            cv2.line(image,(right_shoulder_x,right_shoulder_y),(right_hip_x,right_hip_y),(0,255,255),4)

            cv2.line(image,(right_ear_x,right_ear_y),(right_shoulder_x,right_shoulder_y),(0,0,255),4)


            # displaying angle on hip

            cv2.putText(image,str(int(torso_inclination)),(right_hip_x,right_hip_y),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)
            cv2.putText(image,"Torso Inclination:"+str(int(torso_inclination)),(700,40),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),2)

            cv2.putText(image,str(int(neck_inclination)),(right_shoulder_x,right_shoulder_y),cv2.FONT_HERSHEY_PLAIN,3,(255,255,0),2)
            cv2.putText(image,"Neck Inclination:"+str(int(neck_inclination)),(700,80),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),2)

            
            # mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                    #   landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            cv2.imshow('MediaPipe Pose', image)
            k = cv2.waitKey(1)
            if k == ord('q'):
                break
    video.release()
    cv2.destroyAllWindows()
    return "Yeah! pose landmarks successfully detected :)"


root = Tk()
root.geometry('500x500')
root.resizable(0,0)
root.title('Tkinter GUI')

Label(root,text='Tkinter GUI for MediaPipe',font='comicsansms 14 bold').pack(pady=50)
b1 = Button(root,text='face',bg='black',fg='white',height=1,width=5,command=face).pack(side=LEFT,padx=60,pady=50)
b2 = Button(root,text='squat',bg='black',fg='white',height=1,width=5,command=squat).pack(side=LEFT,padx=60,pady=50)
b3 = Button(root,text='back',bg='black',fg='white',height=1,width=5,command=back).pack(side=LEFT,padx=60,pady=50)


root.mainloop()