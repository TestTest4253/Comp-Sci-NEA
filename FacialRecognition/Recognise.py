from LBPH import LocalBinaryPattern
from sklearn.svm import LinearSVC
from imutils import paths
import cv2
import os
import pickle

desc = LocalBinaryPattern(24, 8)
data = []
labels = []

for imagePath in paths.list_images("FacialRecognition\Faces\Training"):
    image = cv2.imread(imagePath)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hist = desc.describe(grey)
    
    labels.append(imagePath.split(os.path.sep)[-2])
    data.append(hist)

model = LinearSVC(C=100.0, random_state = 42)
model.fit(data, labels)
with open("FacialRecognition\model.pickle", "wb") as f:
    pickle.dump(model, f)
