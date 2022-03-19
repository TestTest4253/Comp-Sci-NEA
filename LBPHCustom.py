from helper import local_binary_pattern, hist, euclidean_distance

import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt

img = "Faces/Seb Atkins/myimage2.png"
GreyImage = "tmp/TestImage.png"
GreyImage2 = "Faces/Oscar White/myimage1.png"

Labels = ["Seb", "James", "Oscar", "Seb"]
Lowest_val = 1000000

# Remove if wanting to display the LBP image
"""
img = local_binary_pattern("Swag2.png")
plt.imshow(img, cmap = "gray", vmin = 0, vmax = 255)
plt.show()
"""

# Remove if wanting to guess the person

lbp1 = hist(local_binary_pattern(GreyImage))
lbp2 = hist(local_binary_pattern(GreyImage2))
"""

People = []
People.append(GreyImage)
People.append(GreyImage2)
People.append(GreyImage3)

TargetHist = hist(local_binary_pattern(People[0]))

Hists = []
for person in People:
    Hists.append(hist(local_binary_pattern(person)))
    
for x in range(len(Hists)):
    val = euclidean_distance(TargetHist, Hists[x])
    print(f"val for {Labels[x]} is {val} ")
    if val < Lowest_val:
        Lowest_val = val
        person = Labels[x]

print(f"Person in image is: {person}, target was {Labels[0]}")
"""


# Remove if wanting to print the histograms
vals = range(len(lbp1))
plt.figure(figsize=(10,8))
plt.subplot(231); plt.bar(vals,lbp1); plt.title("Test"); plt.axis = ("off")
#plt.subplot(232); plt.bar(vals,lbp2); plt.title("Oscar"); plt.axis = ("off")
plt.show()

