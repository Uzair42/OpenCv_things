# Estimate the Camera Response Function 
The camera response function (CRF) describes the non-linear mapping between real-world scene radiance (light intensity) and the pixel brightness values recorded by a digital camera.    

In OpenCV, estimating the CRF is a key step in High Dynamic Range (HDR) imaging pipelines. The library provides specific algorithms to estimate the inverse camera response function from a sequence of images of the same static scene taken at different exposure times.    

---

## OpenCV Implementation
OpenCV's photo module includes classes to calibrate the camera response function, most notably:

- cv.createCalibrateDebevec():    
Implements the algorithm proposed by Paul Debevec and Jitendra Malik. This method minimizes an objective function using a linear system and adds a smoothness term to the result.It requires a set of images with known, varying exposure times.
---
- cv.createCalibrateRobertson():    
Implements the algorithm by Mark Robertson, Sean Borman, and Robert Stevenson. Like the Debevec method, it also requires an exposure sequence and produces a smooth estimate of the inverse CRF. 
---

The output of these calibration functions is typically a 256-length vector (for 8-bit images) for each color channel (R, G, B), representing the inverse response function. This function maps the observed pixel values back to the relative log-exposure or scene radiance values, allowing for the creation of a linear, high dynamic range image. 

---
## Why Estimate the CRF?

- High Dynamic Range Imaging (HDR): The primary use is to combine multiple low dynamic range (LDR) images into a single HDR image that captures a wider range of light details than any single photo could.   

- Computer Vision Applications: Many algorithms in computer vision, such as photometric stereo or color constancy, assume a linear relationship between light in the scene and pixel values. Knowing and inverting the CRF makes these algorithms more accurate and robust.   

-Scientific Measurement: Calibrating the camera's response can turn a consumer-grade camera into a scientific measurement device by providing a predictable, linear relationship for recorded light intensities

