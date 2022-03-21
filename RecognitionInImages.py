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

def create_hists():
	print("MAKING HISTS")
	Lowest_value = 1000000
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
	return Hists, Labels

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

def test_accuracy(query, user, Hists, Label):
	Lowest_value = 1000000
	query_hist = hist(local_binary_pattern(query))
	Hist = Hists
	Labels = Label
	person = None

	for x in range(len(Labels)):
		for y in range(len(Hist[0])):
			val = euclidean_distance(query_hist, Hist[x][y])
			if val < Lowest_value:
				Lowest_value = val
				person = Labels[x]

	print(f"Person is: {person}, person was meant to be: {user}")
	if person == user:
		global Correct
		Correct += 1
	global Total
	Total += 1
"""
Made = 0
global Correct
Correct = 0
global Total
Total = 0

for subject in os.listdir("yalefaces"):
	for folder in os.listdir(f"yalefaces/{subject}"):
		if folder == "Test":
			for image in os.listdir(f"yalefaces/{subject}/{folder}"):
				if Made == 0:
					Hists, Labels = create_hists()
					test_accuracy(f"yalefaces/{subject}/{folder}/{image}", subject, Hists, Labels)
					Made = 1
				else:
					test_accuracy(f"yalefaces/{subject}/{folder}/{image}", subject, Hists, Labels)
print(f"Final accuracy was {(Correct / Total) * 100}%")
"""