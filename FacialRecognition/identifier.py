import numpy as np
import cv2
import pickle
from LBPH import LocalBinaryPattern

detect = True  
Recognise = False
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")
num = 1
labels = {}
recogniser = cv2.face.LBPHFaceRecognizer_create()
recogniser.read("FacialRecognition/trainer.yml")
with open("FacialRecognition/labels.pickle", "rb") as f:
    labels = pickle.load(f)
    labels = {v: k for k, v in labels.items()}

while True:
    _, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        grey, 1.1, 5)
    for (x, y, w, h) in faces:
        roi_grey = grey[y:y+h, x:x+w]
        roi_colour = frame[y:y+h, x:x+w]

        if detect == True:
            colour = (255, 0, 0)
            stroke = 2
            cv2.rectangle(frame, (x, y), (x+w, y+h), colour, stroke)
            img_item = "myimage"+str(num)+".png"
            cv2.imwrite(img_item, roi_colour)
            num += 1
            if num >= 100:
                exit()
    # Displaying the frame
    cv2.imshow("frame", frame)
    if cv2.waitKey(100) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()
