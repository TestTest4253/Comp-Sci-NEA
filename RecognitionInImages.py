from helper import local_binary_pattern, hist, euclidean_distance
import cv2
import numpy as np
import os
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

def add_face(img, user):
	grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts image to greyscale to allow for better recognition
	faces = face_cascade.detectMultiScale(grey_img, scaleFactor = 1.05, minNeighbors= 6, minSize = [30,30])
	for (x, y, w, h) in faces:
		roi_colour = img[y:y+h, x:x+w]
		colour = (255, 0, 0)
		stroke = 2
		cv2.rectangle(img, (x, y), (x+w, y+h), colour, stroke)
		img_item = f"Faces/{user}/myImage0.png"
		cv2.imwrite(img_item, roi_colour)

def identify_face(histogram, user):
	Lowest_val = 1000000000000
	query = histogram
	Database = []
	Person = []
	Labels = []
	start = time.time()
	for x in os.listdir("Faces"):
		num = 0
		Labels.append(x)
		for y in os.listdir(f"Faces/{x}"):
			Person.append(hist(local_binary_pattern(f"Faces/{x}/{y}")))
			num += 1
			if num == 10:
				break
		Database.append(Person)
		Person = []
	for x in range(len(Labels)):
		for y in range(len(Database)):
			val = euclidean_distance(query, Database[x][y])
			if val < Lowest_val:
				Lowest_val = val
				person = Labels[x]
	try:
		P = person
	except:
		person = None
	Correct = (person == user)
	end = time.time()
	print(f"Code guesses: Person is {person}, this guess was {Correct}, time taken: {end-start}")

def detect_face(img):
	grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts image to greyscale to allow for better recognition
	faces = face_cascade.detectMultiScale(grey_img, scaleFactor = 1.05, minNeighbors= 6, minSize = [30,30])
	for (x, y, w, h) in faces:
		roi_colour = img[y:y+h, x:x+w]
		colour = (255, 0, 0)
		stroke = 2
		cv2.rectangle(img, (x, y), (x+w, y+h), colour, stroke)
		img_item = f"tmp/TestImage.png"
		cv2.imwrite(img_item, roi_colour)
