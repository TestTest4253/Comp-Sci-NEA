import numpy as np
from PIL import Image
import cv2
from matplotlib import pyplot as plt

Image = np.array(Image.open("myimage2.png"))
Grey = cv2.cvtColor(Image, cv2.COLOR_RGB2GRAY)

xParam = 8
yParam = 8


plt.style.use("fivethirtyeight")

plt.hist(Grey, bins=256)

plt.title("Grayscale Histogram")
plt.xlabel("grayscale value")
plt.ylabel("pixel count")
plt.show()