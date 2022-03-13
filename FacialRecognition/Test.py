import numpy as np
import cv2
import pickle
from LBPH import LocalBinaryPattern

detect = False  
Recognise = True
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
model = pickle.loads(open("FacialRecognition\model.pickle", "rb").read())
desc = LocalBinaryPattern(24, 8)
while True:
    _, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if Recognise:
        hist = desc.describe(grey)
        prediction = model.predict(hist.reshape(1, -1))
        cv2.putText(frame, prediction[0], (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # Displaying the frame
    cv2.imshow("frame", frame)
    if cv2.waitKey(100) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()