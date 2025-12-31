import cv2 as cv 
import numpy as np

#Capture the Video from the webcam 0
cap = cv.VideoCapture(0)

# Seting the Resolution of camera to HD
cap.set(3,1400)
cap.set(4 ,1400)

#itrate through frames and show video on screen
while True :
 
 ret , frame = cap.read()
 
 # If ret is true then show the image 
 if ret==True:
  cv.imshow("MyCamera",frame)

# For Quite the Camera Window using 'q'
 if cv.waitKey(1) & 0xFF ==ord('q'):
  break
  
  #Release the Resources 
cap.release()
cv.destroyAllWindows()