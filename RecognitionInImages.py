import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

def Detect_Face(img, user):
	grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts image to greyscale to allow for better recognition
	faces = face_cascade.detectMultiScale(grey_img, scaleFactor = 1.05, minNeighbors= 6, minSize = [30,30])
	for (x, y, w, h) in faces:
		print("Face Detected")
		roi_colour = img[y:y+h, x:x+w]
		colour = (255, 0, 0)
		stroke = 2
		cv2.rectangle(img, (x, y), (x+w, y+h), colour, stroke)
		img_item = f"{user}/myImage0.png"
		cv2.imwrite(img_item, roi_colour)

