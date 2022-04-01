from helper import local_binary_pattern, hist, euclidean_distance
import cv2
import numpy as np
import os
import time
from PIL import Image
import ctypes

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")

def create_hists(Dataset):
	Person = []
	for subject in os.listdir(f"{Dataset}"):
		made = False
		num = 0
		for photo in os.listdir(f"{Dataset}/{subject}"):
			if photo.endswith(".txt"):
				made = True
		for photo in os.listdir(f"{Dataset}/{subject}"):
			if made == False:
				if photo.endswith(".png"):
					num += 1
					Person.append(hist(local_binary_pattern(f"Faces/{subject}/{photo}")))
				if num == 10:
					break
		if made == False:
			np.savetxt(f"Faces/{subject}/{subject}'s Hist.txt", Person)
			Person = []	

def identify_face(histogram, user):
	Lowest_val = 1000000000000
	query = histogram
	start = time.time()
	Labels = []
	Hists = []

	for subject in os.listdir("Faces"):
		Labels.append(subject)
		Hists.append(np.loadtxt(f"Faces/{subject}/{subject}'s Hist.txt")) # Loads user's histogram from file path

	for x in range(len(Labels)):
		for y in range(len(Hists)):
			val = euclidean_distance(query, Hists[x][y])
			if val < Lowest_val:
				Lowest_val = val
				person = Labels[x]
	try:
		P = person
	except:
		person = None
	Correct = (person == user)
	end = time.time()
	ctypes.windll.user32.MessageBoxW(0, f"Person is {person}", "Guess", 1) # Displays popup window on the screen

def detect_face(img):
	try:
		grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts image to greyscale to allow for better recognition
	except:
		ctypes.windll.user32.MessageBoxW(0, "Error in assertion, please stop and restart camera", "WARNING", 1)
	faces = face_cascade.detectMultiScale(grey_img, scaleFactor = 1.05, minNeighbors= 6, minSize = [30,30]) # Finds coords of user's face on the webcam
	for (x, y, w, h) in faces:
		roi_colour = img[y:y+h, x:x+w]
		colour = (255, 0, 0)
		stroke = 2
		cv2.rectangle(img, (x, y), (x+w, y+h), colour, stroke)
		img_item = f"tmp/TestImage.png"
		cv2.imwrite(img_item, roi_colour)