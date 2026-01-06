import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)


red=np.uint8([[[0,0,255]]])
hsv_red=cv.cvtColor(red,cv.COLOR_BGR2HSV)
print("hsv red value is ",hsv_red)


while (cv.waitKey(1)) != 27:
    ret, frame=cap.read()
    if not ret:
        print("no frame")
        break
    

      # define range for reg color in HSV 
    lower_red = np.array([0,120,70])
    upper_red = np.array([10,255,255])
    hsv_frame=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    mask1=cv.inRange(hsv_frame,lowerb=lower_red,upperb=upper_red)
    red_image=cv.bitwise_and(frame,frame,mask=mask1)
    cv.imshow("only red color ",red_image)



#------------------------------------------------------------
        # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    hsv_frame=cv.cvtColor(frame,cv.COLOR_BGR2HSV)

    mask=cv.inRange(hsv_frame,lowerb=lower_blue,upperb=upper_blue)
    blue_image=cv.bitwise_and(frame,frame,mask=mask)

    cv.imshow("only blue color ",blue_image)

cap.release()
cap.destroyvAllWindows()