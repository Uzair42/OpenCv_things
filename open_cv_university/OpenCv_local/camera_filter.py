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
     
      def simpleblure(frame):
         return cv.blur(frame,(10,10))
      
      def GuassianBlur(frame):
       return cv.GaussianBlur(frame,(7,7),2.0)
      
      def bilatralblur(frame):
         return cv.bilateralFilter(frame,0,10,10)
      
      def medianblur(frame):
         return cv.medianBlur(frame,7)
      
      def Sharpener(frame):
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
   
      
   def erosion(frame):
      kernel = np.ones((5,5),np.uint8)
      return cv.erode(frame,kernel,iterations=1)
   
   def dilation(frame):
      kernel = np.ones((5,5),np.uint8)
      return cv.dilate(frame,kernel,iterations=1)
   
   def opening(frame):
      kernel = np.ones((5,5),np.uint8)
      return cv.morphologyEx(frame,cv.MORPH_OPEN,kernel)
   
   def closing(frame):
      kernel = np.ones((5,5),np.uint8)
      return cv.morphologyEx(frame,cv.MORPH_CLOSE,kernel)

    
   

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
   
      
      
   def cannyEdge(frame):
      return cv.Canny(frame,100,200)
   def laplacianEdge(frame):
      return cv.Laplacian(frame,0,ksize=(6,6))
   def sobelEdge(frame):
      sobelx = cv.Sobel(frame,cv.CV_64F,1,0,ksize=5)
      sobely = cv.Sobel(frame,cv.CV_64F,0,1,ksize=5)
      return sobelx, sobely   
   
   




class cameraFilter:
      def __init__(self,filter_type=NONE):
         self.filter_type=filter_type
       
         


      def applyFilter(self,frame):


         
         #for Blur
         if self.filter_type==BLUR:
            blurObj=blurClass
            return  blurObj.GuassianBlur(frame)
         elif self.filter_type==CANNY:
            return cv.Canny(frame,80,130)
         elif self.filter_type==EDGE_DETECTION:
            return cv.Laplacian(frame,1,ksize=17)
         
         else:
            return cv.flip(frame,1)
          
      

def main():

   
  
   filter=cameraFilter(CANNY)
   filter_2=cameraFilter(BLUR)
   edge_3=cameraFilter(EDGE_DETECTION)

   # objEdgeDetector=EdgeDetection()

   # objThresholding=Thresholding()

   objBlur=blurClass

   objmarphogy=MorphologicalOperations




   
   cap=cv.VideoCapture(0)
   if cap.isOpened:
      print("Resource is availble ")
   
# ----------- using while loop , extract frame using single videocapture object and process frame for different purposes -------
   while cv.waitKey(1) != 27:
      ret , frame = cap.read()
      if not ret:
         print("no frame availbe")
         break
      # First Window , with filter object no 1
      filter_frame=filter.applyFilter(frame=frame)
      cv.imshow(str(filter.filter_type),filter_frame)

      # Second Window , with filter object no 2
      filter_frame=filter_2.applyFilter(frame=frame)
      cv.imshow(str(filter_2.filter_type),filter_frame)

      # 3rd windoe with edge detections
      edge_frame=edge_3.applyFilter(frame)
      cv.imshow("edge lap",edge_frame)

      # 4th Window Threshold
      sharperner_frame=objBlur.Sharpener(frame)
      cv.imshow("Thresold ",sharperner_frame)

      # 5th Window Threshold
      objmarphogy_frame=objmarphogy.dilation(frame)
      cv.imshow("marhpholgy ",objmarphogy_frame)

   cap.release()
   cv.destroyAllWindows()
      

if __name__ == "__main__":
   main()





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
