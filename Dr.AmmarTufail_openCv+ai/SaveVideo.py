import cv2 as cv 
import numpy as np

cap = cv.VideoCapture(0)




# Define the codec and create VideoWriter object to save the video in grayscale
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('output_bw.avi', fourcc, 20.0, (640, 480), isColor=False)



while True:
    ret , frame = cap.read()

    if ret==True:
        out.write(frame)
        cv.imshow("recorded Stream",frame)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break


cap.release()
out.release()
cv.destroyAllWindows()