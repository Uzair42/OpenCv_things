import cv2 as cv
import numpy as np

img_sun="/home/uzair/Python/OpenCv_things/open_cv_university/openCv_python_notebooks/image.png"
img_piano="/home/uzair/Python/OpenCv_things/open_cv_university/openCv_python_notebooks/Piano_Sheet_Music.png"

img=cv.imread(img_piano)
cv.imshow("orginal image",img)

box=img.copy()

# simple blur image 
cv.imshow("simple blur",cv.blur(img.copy(),(10,10)))

# boxfilter image blur
cv.imshow("box blur ", cv.boxFilter(img.copy(),0,(8,8)))
cv.imshow("box blur 1 ", cv.boxFilter(img.copy(),-1,(14,14)))
cv.imshow("box blur  2", cv.boxFilter(img.copy(),-1,(44,44)))

# Gaussian blur
cv.imshow("Gaussian blur1",cv.GaussianBlur(img.copy(),(7,7),0))
cv.imshow("Gaussian blur2",cv.GaussianBlur(img.copy(),(7,7),2.0))

# median blur
cv.imshow("Median blur 1",cv.medianBlur(img.copy(),7))


# Bilateral filter
cv.imshow("Bilatralfilter 1",cv.bilateralFilter(img.copy(),4,75,75))

 
# 5. Custom Sharpening Filter
cus = img.copy()
kernel = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
sharpened = cv.filter2D(cus, -1, kernel)
cv.imshow('Sharpened', sharpened)
cv.imwrite('sharpened.jpg', sharpened)

cv.waitKey(0)
cv.destroyAllWindows()
