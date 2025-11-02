import cv2 as cv
import numpy as np

cap=cv.VideoCapture('video/group.mp4')
count=0

while True:
    success , frame = cap.read()
    if success==True:
        cv.imwrite(f"frames/{count}frame.png",frame)
    else:
        break
    count=count+1
cap.release()