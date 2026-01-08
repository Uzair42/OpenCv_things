import cv2 as cv
import numpy as np 

import threading


PREVIEW = 1
THRESHOLD=2
BLUR=3
MORPHOLOGY=4
EDGE_DETECTION=5
CANNY=11
COLOR_SPACE=6
BITWISE=7
CONTOUR=8
SHARPEN=9
NONE=0

class cvtColorClass:
    def __init__(self,color,frame):
      self.color=color
      self.frame=frame
      
    def toGray(self):
       return cv.cvtColor(self.frame,cv.COLOR_BGR2GRAY)
    
    def toRGB(self):
       return cv.cvtColor(self.frame,cv.COLOR_BGR2RGB)
    
    def toHSV(self):
       return cv.cvtColor(self.frame,cv.COLOR_BGR2HSV)
    

class blurClass:
      
      def __init__(self,frame):
         self.frame=frame
      

      def simpleblure(self):
         return cv.blur(self.frame,(10,10))
      
      def GuassianBlur(self):
       return cv.GaussianBlur(self.frame,(7,7),2.0)
      
      def bilatralblur(self,frame):
         return cv.bilateralFilter(frame,0,10,10)
      
      def medianblur(self,frame):
         return cv.medianBlur(frame,7)
      
      def Sharpener(self,frame):
         kernal = np.array([[0,-1,0],
                            [-1,5,-1],
                            [0,-1,0]])
         return cv.filter2D(frame,-1,kernel=kernal)
      

class BitwiseOperations:
   def __init__(self,frame):
      self.frame=frame
      
   def andBitwise(self):
      return cv.bitwise_and(srlf.frame)
   
   def orBitwise(self):
      return cv.bitwise_or(self.frame)
   
   def notBitwise(self):
      return cv.bitwise_not(self.frame)
   
   def xorBitwise(self):
      return cv.bitwise_xor(self.frame)
   
class MorphologicalOperations:
   def __init__(self,frame):
      self.frame=frame
      
   def erosion(self):
      kernel = np.ones((5,5),np.uint8)
      return cv.erode(self.frame,kernel,iterations=1)
   
   def dilation(self):
      kernel = np.ones((5,5),np.uint8)
      return cv.dilate(self.frame,kernel,iterations=1)
   
   def opening(self):
      kernel = np.ones((5,5),np.uint8)
      return cv.morphologyEx(self.frame,cv.MORPH_OPEN,kernel)
   
   def closing(self):
      kernel = np.ones((5,5),np.uint8)
      return cv.morphologyEx(self.frame,cv.MORPH_CLOSE,kernel)

    
   

class Thresholding:
   def __init__(self,frame):
      self.frame=frame
      
   def binaryThreshold(self):
      _,thresh=cv.threshold(self.frame,127,255,cv.THRESH_BINARY)
      return thresh
   
   def binaryInvThreshold(self):
      _,thresh=cv.threshold(self.frame,127,255,cv.THRESH_BINARY_INV)
      return thresh
   
   def truncThreshold(self):
      _,thresh=cv.threshold(self.frame,127,255,cv.THRESH_TRUNC)
      return thresh
   
   def toZeroThreshold(self):
      _,thresh=cv.threshold(self.frame,127,255,cv.THRESH_TOZERO)
      return thresh
   
   def toZeroInvThreshold(self):
      _,thresh=cv.threshold(self.frame,127,255,cv.THRESH_TOZERO_INV)
      return thresh
   
class ContourDetection:
   def __init__(self,frame):
      self.frame=frame
      
   def findContours(self):
      contours, hierarchy = cv.findContours(self.frame, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
      return contours, hierarchy 
   def drawContours(self,contours):
      img_contours = self.frame.copy()
      cv.drawContours(img_contours, contours, -1, (0, 255, 0), 3)
      return img_contours
   

class EdgeDetection:
   def __init__(self,frame):
      self.frame=frame
      
   def cannyEdge(self):
      return cv.Canny(self.frame,100,200)
   def laplacianEdge(self):
      return cv.Laplacian(self.frame,cv.CV_64F)
   def sobelEdge(self):
      sobelx = cv.Sobel(self.frame,cv.CV_64F,1,0,ksize=5)
      sobely = cv.Sobel(self.frame,cv.CV_64F,0,1,ksize=5)
      return sobelx, sobely   
   
   




class cameraFilter:
      def __init__(self,cameraIndex=0,filter_type=NONE):
         self.filter_type=filter_type
         self.cameraIndex=cameraIndex
         self.cap=cv.VideoCapture(self.cameraIndex)
         if self.cap.isOpened:
            print("Camera is opened")


      def takeResourse(self,cap):
         self.cap.release()
         cv.destroyAllWindows()

      def applyFilter(self,frame):


         
         #for Blur
         if self.filter_type==BLUR:
            blurObj=blurClass(frame)
            return  blurObj.GuassianBlur()
         elif self.filter_type==CANNY:
            return cv.Canny(frame,80,130)
         
         else:
            return cv.flip(frame,1)
          
      

def main(self,windowName):
   cv.namedWindow(windowName,cv.WINDOW_NORMAL)

   while cv.waitKey(1) != 27 :
   ret,frame=self.cap.read()
   if not ret:
      print("no frame ")
   frame_edit=self.applyFilter(frame)
   cv.imshow(windowName,frame_edit)

   self.cap.release()
   print("camera closed")
   cv.destroyAllWindows()




##-------------------Learning ----------------------------------------
# my idea was to initate two object and perform different task at same time
#  using single webcam or single camera source , 
# i try to use multithreading approch , but failed as i think camera resource only availble 
# for other thread it has to wait for first thread to somehow finsh
#  in my case both object have their own showStream function which create their own videoCapture Resource self.cap
            
# objCameraFilter=cameraFilter(0,BLUR)
# # objCameraFilter.ShowStream("CANNY")


# objCameraFilter1 = cameraFilter(0, NONE)

# threads = []

# t = threading.Thread(target=lambda: objCameraFilter1.ShowStream("NONE"))
# t2 = threading.Thread(target=lambda: objCameraFilter.ShowStream("CANNY"))

# t.start()
# t2.start()

# t.join()
# t2.join()

# print("All Done")

#-------------------------------------------------------------------------------------
