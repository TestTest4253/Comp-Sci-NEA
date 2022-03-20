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

"""
def create_hists(user):
	for x in os.listdir(f"Faces/{user}"):
		if x == "histogram.txt":
			continue
		with open(f"Faces/{user}/histogram.txt", "w+") as file:
			file.write(str(hist(local_binary_pattern(f"Faces/{user}/{x}"))))
		break
	with open(f"Faces/{user}/histogram.txt", "r") as file:
		item = file.read()
		print(np.fromstring(item, float))
"""

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

def test_accuracy(query, user):
	Lowest_value = 1000000
	query_hist = hist(local_binary_pattern(query))
	Person = []
	Labels = []
	Hists = []
	for subject in os.listdir("yalefaces"):
		Labels.append(subject)
		for folder in os.listdir(f"yalefaces/{subject}"):
			if folder == "Train":
				for image in os.listdir(f"yalefaces/{subject}/{folder}"):
					Person.append(hist(local_binary_pattern(f"yalefaces/{subject}/{folder}/{image}")))
				Hists.append(Person)
				Person = []

	for x in range(len(Labels)):
		for y in range(len(Hists)):
			val = euclidean_distance(query_hist, Hists[x][y])
			if val < Lowest_value:
				Lowest_val = val
				person = Labels[x]

	print(f"Person is: {person}, person was meant to be: {user}")

for subject in os.listdir("yalefaces"):
	for folder in os.listdir(f"yalefaces/{subject}"):
		if folder == "Test":
			for image in os.listdir(f"yalefaces/{subject}/{folder}"):
				test_accuracy(f"yalefaces/{subject}/{folder}/{image}", {subject})
