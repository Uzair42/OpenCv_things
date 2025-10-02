import cv2 as cv

img=cv.imread('pics/image.png')
dst=cv.xphoto.oilPainting(img,7,1)  
cv.imshow('oil',dst)
cv.waitKey(0)
cv.destroyAllWindows() 
cv.imwrite('pics/oil_painting.png',dst)
