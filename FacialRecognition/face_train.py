import os
from PIL import Image
import numpy as np
import cv2
import pickle

basedir = os.path.dirname(os.path.abspath(__file__))
imagedir = os.path.join(basedir, "Faces")
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recogniser = cv2.face.LBPHFaceRecognizer_create()
current_id = 0
label_ids = {}
x_train = []
y_labels = []

for root, dirs, files in os.walk(imagedir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(
                path)).replace(" ", "-").lower()
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            pil_image = Image.open(path).convert("L")  # Greyscale
            size = (550, 550)
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            faces = face_cascade.detectMultiScale(image_array, 1.1, 5)
            for (x, y, w, h) in faces:
                ROI = image_array[y:y+h, x:x+w]
                x_train.append(ROI)
                y_labels.append(id_)

with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

recogniser.train(x_train, np.array(y_labels))
recogniser.save("trainer.yml")
