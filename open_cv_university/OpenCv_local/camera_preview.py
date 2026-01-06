import cv2 as cv 
import sys

# Setting up Default camera index
s=0
if len(sys.argv)>1:
    s=int(sys.argv[1])

# Setting up the window name 

window_name="Camera Preview"
preview_window=cv.namedWindow(window_name,cv.WINDOW_NORMAL)

# Capturing video 
source = cv.VideoCapture(s) 


while cv.waitKey(1) != 27 : # For Escape key 
    has_frame , frame = source.read()
    if not has_frame:
            print("No frame captured from camera. Exiting")
            break
    cv.imshow(window_name,frame)
source.release()
cv.destroyAllWindows()
 
