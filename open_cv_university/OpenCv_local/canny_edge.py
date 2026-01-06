import cv2 as cv

source=cv.VideoCapture(0)

while cv.waitKey(1) != 27:
    ret, frame= source.read()
    frame=cv.flip(frame,1)
    if not ret:
        print("no frame")
        break
    else:
        gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        img_edg=cv.Canny(gray,90,100)
        cv.imshow("canny edges 90 sy 100 ",img_edg)
        img_edg=cv.Canny(gray,50,100)
        cv.imshow("canny edges 50 sy 100 ",img_edg)
        gray=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        img_edg=cv.Canny(gray,90,150)
        cv.imshow("canny edges 90 sy 150 ",img_edg)
        img_edg=cv.Canny(gray,50,150)
        cv.imshow("canny edges 50 sy 150 ",img_edg)
        img_edg=cv.Canny(gray,30,80)
        cv.imshow("canny edges 30 sy 80 ",img_edg)
        img_edg=cv.Canny(gray,10,50)
        cv.imshow("canny edges 10 sy 50 ",img_edg)


source.release()
cv.destroyAllWindows()