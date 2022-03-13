from helper import local_binary_pattern

import numpy as np
from PIL import Image
import cv2
from matplotlib import pyplot as plt
import math

Image = np.array(Image.open("myImage2.png"))
GreyImage = cv2.cvtColor(Image, cv2.COLOR_RGB2GRAY)

lbp = np.array(local_binary_pattern(GreyImage), np.uint8)
plt.imshow(lbp, cmap = "gray", vmin = 0, vmax = 255)
plt.show()

(hist, _) = np.histogram(lbp.ravel(), bins = np.arange(0,11))
hist = hist.astype("float")
hist /= (hist.sum() + 1e-6)