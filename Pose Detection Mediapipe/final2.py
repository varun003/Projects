import numpy as np
import math as m
import cv2
import mediapipe as mp

# Calculate angle.

def findAngle(x1, y1, x2, y2):
    theta = m.acos( (y2 -y1)*(-y1) / (m.sqrt((x2 - x1)**2 + (y2 - y1)**2 ) * y1) )
    degree = int(180/m.pi)*theta
    degree = degree - 90
    return degree

good_frames = 0
bad_frames = 0

# initialzing mediapipe

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Video Writing

path = 'video/body_posture.mp4'
cap = cv2.VideoCapture(path)

fps = int(cap.get(cv2.CAP_PROP_FPS))
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame = (w,h)
print('frame:',frame)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_output = cv2.VideoWriter('output1.mp4',fourcc,fps,frame)

while cap.isOpened():
    success,img = cap.read()
    if not success:
        print('null frame')
        break
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result = pose.process(img)
    
    # converting image back to BGR

    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    lm = result.pose_landmarks
    lmPose = mp_pose.PoseLandmark


    # landmarking coordinates

    right_shoulder_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
    right_shoulder_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

    right_hip_x = int(lm.landmark[lmPose.RIGHT_HIP].x * w)
    right_hip_y = int(lm.landmark[lmPose.RIGHT_HIP].y * h)

    right_knee_x = int(lm.landmark[lmPose.RIGHT_KNEE].x * w)
    right_knee_y = int(lm.landmark[lmPose.RIGHT_KNEE].y * h)


    # finding torso's inclination
    torso_inclination = findAngle(right_shoulder_x,right_shoulder_y,right_hip_x,right_hip_y)
    # print(torso_inclination)


    if torso_inclination < 75:
        good_frames = 0
        bad_frames = bad_frames + 1
    if 75 <= torso_inclination <= 110:
        good_frames = good_frames + 1
        bad_frames = 0

    good_time = (1/fps) * good_frames
    bad_time = (1/fps) * bad_frames 


    # lamdmarking torso's inclination
    cv2.circle(img,(right_shoulder_x,right_shoulder_y),5,(0,0,255),-1)
    cv2.circle(img,(right_hip_x,right_hip_y),5,(0,0,255),-1)

    # joining landmarks
    cv2.line(img,(right_shoulder_x,right_shoulder_y),(right_hip_x,right_hip_y),(0,255,255),2)

    # displaying angle on hip

    cv2.putText(img,str(int(torso_inclination)),(right_hip_x,right_hip_y),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.putText(img,"Torso Inclination:"+str(int(torso_inclination)),(10,40),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),1)
    video_output.write(img)
    
    # cv2.imshow('output',img)

    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     break

print('good time:',good_time)
print('bad time:',bad_time)

print('Finished')
    

cap.release()
# cv2.destroyAllWindows()
video_output.release()

# cap.release()
# cv2.destroyAllWindows()

