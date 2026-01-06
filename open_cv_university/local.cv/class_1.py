import cv2 as cv
import numpy as np



img= cv.imread("image.png")


# ---------------- Read the image and show on window frame for give arg secondds
windowName=cv.namedWindow("window 1")
cv.imshow(windowName,img)
cv.waitKey(3000) # Reading image for just few seconds
cv.destroyWindow(windowName)


#-------------Using the while Loop to hold the window untill q is pressed 
Alive =True
while Alive:
    cv.imshow(windowName,img)
    if ord("q") ==(cv.waitKey(1)):
        Alive=False
cv.destroyWindow(windowName)

cv.destroyAllWindows()


   