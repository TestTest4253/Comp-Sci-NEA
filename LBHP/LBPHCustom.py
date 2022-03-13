from helper import local_binary_pattern, hist, euclidian_distance

import numpy as np
from PIL import Image
import cv2
from matplotlib import pyplot as plt

GreyImage = cv2.cvtColor(
    np.array(Image.open("myImage2.png")), cv2.COLOR_RGB2GRAY)
GreyImage2 = cv2.cvtColor(
    np.array(Image.open("myImage14.png")), cv2.COLOR_RGB2GRAY)
GreyImage3 = cv2.cvtColor(
    np.array(Image.open("myImage83.png")), cv2.COLOR_RGB2GRAY)
GreyImage4 = cv2.cvtColor(
    np.array(Image.open("myImage3.png")), cv2.COLOR_RGB2GRAY)

Labels = ["Seb", "James", "Oscar"]
Lowest_val = 1000000

People = []
People.append(GreyImage)
People.append(GreyImage2)
People.append(GreyImage3)

TargetHist = hist(local_binary_pattern(People[2]))

Hists = []
for person in People:
    Hists.append(hist(local_binary_pattern(person)))

for x in range(len(Hists)):
    val = euclidian_distance(TargetHist, Hists[x])
    if val < Lowest_val:
        Lowest_val = val
        person = Labels[x]