import cv2 as cv
import sys 
import numpy 





# Filter Switching 
PREVIEW=1
CANNY = 2
BLUR=3
FEATURES=4
BILATERAL=5



# for feature parameter setting
feature_params = dict(maxCorners=500, qualityLevel=0.2, minDistance=15, blockSize=9)
# for camera index default zero for webcame
s=0

# command line argument as list of string , argv[0]->is script 
# and other represents argument passs to command line 
# file.py argumentstr -> argv[1]will have argumentstr
if len(sys.argv)>1 :
    s=sys.argv[1]

#Window on which frame show
# windoName=cv.namedWindow("Filter Camera ",cv.WINDOW_NORMAL)


result=None
image_filter=PREVIEW
alive=True

key = cv.waitKey(1)


cap = cv.VideoCapture(s)
if cap.isOpened:
    print("video capture is inialized ")


while alive:

    ret , frame= cap.read()
    if not ret:
        print("no frame found")
        break
    # cv.imshow("orginalwindow ",frame)
    
    frame = cv.flip(frame, 1)

    if image_filter == PREVIEW:
        result = frame
        print("preview")
    elif image_filter == CANNY:
        result = cv.Canny(frame, 80, 150)
        print("Canny")
    elif image_filter==BILATERAL:
        print("Bilateral")
        result=cv.bilateralFilter(frame, d=20, sigmaColor=20, sigmaSpace=50)
    elif image_filter == BLUR:
        print("blur")
        result = cv.blur(frame, (13, 13))
    elif image_filter == FEATURES:
        print("feature")
        result = frame
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        corners = cv.goodFeaturesToTrack(frame_gray, **feature_params)
        if corners is not None:
            for x, y in numpy.float32(corners).reshape(-1, 2):
                i,j=int(x), int(y)
                print(i,j)
                cv.circle(result, (i,j), 10, (0, 255, 0), 1)
            
    cv.imshow("windoName",result)

    key = cv.waitKey(1)

    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False
    elif key == ord("C") or key == ord("c"):
        image_filter = CANNY
    elif key == ord("B") or key == ord("b"):
        image_filter = BLUR
    elif key == ord("F") or key == ord("f"):
        image_filter = FEATURES
    elif key == ord("x") or key== ord("X"):
        image_filter=BILATERAL
    elif key == ord("P") or key == ord("p"):
        image_filter = PREVIEW

    


cap.release()
cv.destroyAllWindows()


