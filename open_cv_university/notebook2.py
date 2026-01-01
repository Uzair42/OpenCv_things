# # Basic Image Manipulations
# %% #codecell


import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

img= cv.imread("image.png")
plt.figure(figsize=(10,6))
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.axis('off')
plt.show()





# %%
# accessing the image and manipulating pixels


# %%
#image resizing 


# %%
#image cropping



# %%
# image flipping 



# %%
