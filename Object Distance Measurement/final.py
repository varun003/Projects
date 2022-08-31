import cv2
import numpy as np

def object(img):
    
    width = 0
    
    img = cv2.resize(img,(0,0),None,0.3,0.3)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(9,9),0)
    edged = cv2.Canny(blur,50,100)
    edged = cv2.dilate(edged,None,iterations=2)
    edged = cv2.erode(edged,None,iterations=2)

    threshold = 50

    ret,thresh_img = cv2.threshold(edged,threshold,255,cv2.THRESH_BINARY)
    cnts,hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = [x for x in cnts if cv2.contourArea(x) > 10000]


    cv2.drawContours(img,cnts,-1,(0,0,255),2)
    c = max(cnts,key = cv2.contourArea)

    x,y,w,h = cv2.boundingRect(c)

    cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
    
    width = w
    
    return width

    ## Focal Length

def FocalLength(measured_distance,real_width,width_in_pixel):
    focal_length = (width_in_pixel*measured_distance)/real_width
    return focal_length

 ## Distance Finder
def DistanceFinder(focal_length,known_width,width_in_pixel):
    distance = (known_width*focal_length)/width_in_pixel
    return distance

image = cv2.imread('images/image1.jpg')

width_in_pixel = object(image)
print('Width in Pixels:',width_in_pixel,'pixels')

known_distance = 30
known_width = 7

focal_length = FocalLength(known_distance,known_width,width_in_pixel)

focal_length = int(focal_length)

print('Focal Length:',focal_length,'cm')
# print(type(focal_length))

distance = DistanceFinder(focal_length,known_width,width_in_pixel)
print('Distance in cms:',round(distance,2),'cm')

