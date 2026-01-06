import cv2 as cv
import numpy as np


img=cv.imread("open_cv_university/Adaptive_thresholding.png")
img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
source=cv.VideoCapture(0)

w=int(source.get(3))
h=int(source.get(4))

img=cv.resize(img,(w,h))
mask=cv.imread("open_cv_university/circle.jpg")
mask=cv.cvtColor(mask,cv.COLOR_BGR2GRAY)
mask=cv.resize(mask,(w,h))

aviVideoWriter=cv.VideoWriter("firstOpenCvVideoWriter.avi",cv.VideoWriter_fourcc("M", "J", "P", "G"),10,(w,h))
mp4VideoWriter=cv.VideoWriter("first.mp4",cv.VideoWriter_fourcc(*"XVID"),10,(w,h))

rectangal=np.zeros((w,h),dtype="uint8")
cv.rectangle(rectangal, (25, 25), (275, 275),255,-1)

while cv.waitKey(1) != 27:
    ret,frame=source.read()
    frame=cv.flip(frame,1)
    frame=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    if not ret:
        print("no frame")
        break
    else:
        cv.putText(frame,"Muhammad Uzair",(200,200),cv.FONT_HERSHEY_PLAIN,2.0,255,2,cv.LINE_4)
        # cv.adaptiveThreshold(frame,130,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,12,20)

        # isgod,Frame=cv.threshold(frame,120,255,cv.THRESH_TRUNC)
        # Frame=cv.bitwise_not(frame)
        # Frame=cv.bitwise_xor(img,frame)
        # Frame=cv.bitwise_and(img,frame,mask=mask)
        Frame=cv.bitwise_and(img,frame)
        
        
        cv.imshow("recording...",Frame)
        # aviVideoWriter.write(frame)
        # mp4VideoWriter.write(frame)
source.release()
aviVideoWriter.release()
mp4VideoWriter.release()
cv.destroyAllWindows()