# Canny edge detector

- The Canny edge detector is a widely used, multi-stage algorithm in computer vision for identifying robust, thin, and continuous edges within an image.  
- In OpenCV, this algorithm is implemented in a single, convenient function, cv2.Canny() in Python.    
- The primary goal of Canny is to transform an image into a binary "__edge map__," where object boundaries are highlighted in white against a black background 


---

## How the Canny Algorithm Works
The algorithm follows a series of steps to ensure __accurate and noise-resistant__ edge detection: 

   - __Noise Reduction__ A Gaussian filter is applied to the image to smooth out minor intensity variations and reduce noise that could otherwise produce false edges.   
---
   - __Gradient Calculation__ The algorithm computes the intensity gradients (changes in pixel brightness) of the smoothed image using operators like the __Sobel filter__ . This determines the __strength__ and __direction__ of potential edges at each pixel.   
---
   - __Non-Maximum Suppression__ This step __thins__ the edges to __one-pixel__ width by suppressing any pixels that are not local maxima along the gradient direction.   
 ---  
   - __Hysteresis Thresholding__ This is the final stage, using two thresholds: a high (__maxVal__) and a low (__minVal__) threshold.
       - Pixels with a gradient __above maxVal__ are immediately classified as __strong__, sure __edges__.
       - Pixels __below minVal__ are discarded as __non-edges__.
       - Pixels __between__ the two thresholds are classified as __weak edges__ and are only kept __if__ they are  connected to a __strong edge__ pixel. This ensures edge continuity and reduces noise
---

## Using cv2.Canny() in OpenCV
The function simplifies the entire process. A basic Python implementation looks like this:

```python
import cv2

# Load the image in grayscale (highly recommended for best results)
image = cv2.imread('your_image.jpg', cv2.IMREAD_GRAYSCALE)

# Apply Canny edge detection
# Common practice is to use a high:low ratio between 2:1 and 3:1
edges = cv2.Canny(image, threshold1=50, threshold2=150)

# Display the result (example)
cv2.imshow('Canny Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

```