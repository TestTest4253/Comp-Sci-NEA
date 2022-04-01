from helper import local_binary_pattern, euclidean_distance, User_IDs, hist, backup_files, show_hist
from RecognitionInImages import identify_face, detect_face, create_hists

import os
import urllib
from tkinter import *
import tkinter as tk
import pyrebase
import cv2
import threading
from PIL import Image, ImageTk

global DEBUG
DEBUG = False


firebase_config = {"apiKey": "AIzaSyDbs8Yl971Tqhu4VRXHn3kpRhORmUIk-oo",
                   "authDomain": "computer-science-nea-8f6be.firebaseapp.com",
                   "projectId": "computer-science-nea-8f6be",
                   "storageBucket": "computer-science-nea-8f6be.appspot.com",
                   "messagingSenderId": "231523471417",
                   "appId": "1:231523471417:web:2fd16b7b8003693e0f7de8",
                   "measurementId": "G-9TGMPRHP0R",
                   "databaseURL": "https://computer-science-nea-8f6be.firebaseio.com"}

# Paths
assets = "Assets/"
LOCAL_USER_IDS = "tmp/UserIDs.txt"
CLOUD_USER_IDS = "Credentials/UserIDs.txt"
FACES_DIRECTORY = "Faces"

# Functions

def GetStarted(WelcomeCanvas, test_recognition,
               face_recognition, logout, backup, first_name, last_name, get_started, storage, LOCAL_USER_IDS, CLOUD_USER_IDS):
    if DEBUG:
        print("Getting Started")
    if first_name.get() and last_name.get() != "":
        first_name = first_name.get().capitalize()
        last_name = last_name.get().capitalize()
        global full_name
        full_name = first_name + " " + last_name
        """User_IDs(first_name, last_name,
                                         storage, LOCAL_USER_IDS, CLOUD_USER_IDS)"""
        tk.Misc.lift(WelcomeCanvas, aboveThis=None)
        test_recognition.lift()
        face_recognition.lift()
        logout.lift()
        backup.lift()
        first_name.lower()
        last_name.lower()
        get_started.lower()

def log_out(LoginCanvas, test_recognition,
            face_recognition, logout, backup, first_name, last_name, get_started, faces_dir):
    if DEBUG:
        print("Logging out")
    tk.Misc.lift(LoginCanvas, aboveThis=None)
    test_recognition.lower()
    face_recognition.lower()
    logout.lower()
    backup.lower()
    first_name.lift()
    last_name.lift()
    get_started.lift()

def facial_recognition(WebcamCanvas, backup, logout, face_recognition, test_recognition, Start_camera_button, Stop_camera_button, back_button):
    global ADDING
    ADDING = False
    tk.Misc.lift(WebcamCanvas, aboveThis=None)
    backup.lower()
    logout.lower()
    face_recognition.lower()
    test_recognition.lower()
    Start_camera_button.lift()
    Stop_camera_button.lift()
    back_button.lift()

def add_user(first_name, last_name, WebcamCanvas, backup, logout, face_recognition, test_recognition, Start_camera_button, Stop_camera_button, back_button):
    global ADDING
    ADDING = True
    name = first_name.get().capitalize() + " " + last_name.get().capitalize()
    try:
        os.mkdir(f"Faces/{name}")
    except FileExistsError:
        pass
    tk.Misc.lift(WebcamCanvas, aboveThis=None)
    backup.lower()
    logout.lower()
    face_recognition.lower()
    test_recognition.lower()
    Start_camera_button.lift()
    Stop_camera_button.lift()
    back_button.lift()

def back(WelcomeCanvas,backup, logout, face_recognition, test_recognition, back_arrow, Stop_camera, Start_camera):
    tk.Misc.lift(WelcomeCanvas, aboveThis=None)
    backup.lift()
    logout.lift()
    face_recognition.lift()
    test_recognition.lift()
    back_arrow.lower()
    Stop_camera.lower()
    Start_camera.lower()

def start_button(videoloop_stop):
    thread = threading.Thread(target = videoLoop, args = (videoloop_stop, )).start() # Camera running on different thread to prevent freezing

def stop_button(videoloop_stop):
    videoloop_stop[0] = True
    if ADDING == False:
        lbp = local_binary_pattern("tmp/TestImage.png")
        os.remove("tmp/TestImage.png")
        histo = hist(lbp)
        identify_face(histo, full_name)
    if ADDING == True:
        create_hists("Faces")


def videoLoop(mirror = False):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 832)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 518)

    while True:
        _, frame = cap.read()
        if mirror == True:
            frame = frame[::-1]
        if ADDING == True:
            add_face(frame, full_name)
        else:
            detect_face(frame)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Converts image from openCV color format to normal color format
        image = Image.fromarray(image) # PIL image format
        Tkimage = ImageTk.PhotoImage(image) # Swapped to tkinter format
        panel = tk.Label(image=Tkimage) # Sets Label to contain the image
        panel.image = Tkimage
        panel.place(x=84, y=0)

        # Switcher function
        if videoloop_stop[0]:
            videoloop_stop[0] = False
            panel.destroy()
            break

def add_face(img, user):
    global num
    num = num
    while num != 50:
        print(num)
        grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # Converts image to greyscale to allow for better recognition
        faces = face_cascade.detectMultiScale(grey_img, scaleFactor = 1.05, minNeighbors= 6, minSize = [30,30]) # Calculates coords on img for face location
        for (x, y, w, h) in faces:
            roi_colour = img[y:y+h, x:x+w]
            colour = (255, 0, 0)
            stroke = 2
            cv2.rectangle(img, (x, y), (x+w, y+h), colour, stroke)
            img_item = f"Faces/{user}/myImage{num}.png" # Iterating through the faces adding to user file
            cv2.imwrite(img_item, roi_colour) 
            num += 1

videoloop_stop = [False] # Toggle variable
global num
num = 0
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml") # Used to find face on the image


# GUI Creation
root = Tk()

root.geometry("1000x600")
root.configure(bg="#ffffff")

# Welcome Screen
WelcomeCanvas = Canvas(
    root,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")
WelcomeCanvas.place(x=0, y=0)

face_recognition_img = PhotoImage(file=assets + f"Welcome_Face.png")
face_recognition = Button(
    image=face_recognition_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_user(first_name, last_name, WebcamCanvas, backup, logout, face_recognition, test_recognition, Start_camera_button, Stop_camera_button, back_button),
    relief="flat")

face_recognition.place(
    x=555, y=198,
    width=339,
    height=53)

test_recognition_img = PhotoImage(file=assets + f"Welcome_Test.png")
test_recognition = Button(
    image=test_recognition_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: facial_recognition(WebcamCanvas, backup, logout, face_recognition, test_recognition, Start_camera_button, Stop_camera_button, back_button),
    relief="flat")

test_recognition.place(
    x=556, y=293,
    width=339,
    height=53)

logout_img = PhotoImage(file=assets + f"Welcome_Logout.png")
logout = Button(
    image=logout_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: log_out(LoginCanvas, test_recognition,
                            face_recognition, logout, backup, first_name, last_name, get_started, FACES_DIRECTORY),
    relief="flat")

logout.place(
    x=662, y=395,
    width=126,
    height=53)

backup_img = PhotoImage(file=assets + f"Welcome_info.png")
backup = Button(
    image=backup_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: backup_files(storage, FACES_DIRECTORY),
    relief="flat")

backup.place(
    x=970, y=570,
    width=30,
    height=30)

WebcamCanvas = Canvas(
    root,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")

Start_camera_img = PhotoImage(file=assets + f"StartCamera.png")
Start_camera_button = Button(
    image = Start_camera_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda: start_button(videoloop_stop),
    relief = "flat")

Start_camera_button.place(
    x = 88, y = 534,
    width = 400,
    height = 49)

Stop_camera_img = PhotoImage(file=assets + f"StopCamera.png")
Stop_camera_button = Button(
    image = Stop_camera_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda: stop_button(videoloop_stop),
    relief = "flat")

Stop_camera_button.place(
    x = 516, y = 534,
    width = 400,
    height = 49)

back_button_img = PhotoImage(file=assets + f"BackArrow.png")
back_button = Button(
    image = back_button_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda: back(WelcomeCanvas, backup, logout, face_recognition, test_recognition, back_button, Start_camera_button, Stop_camera_button),
    relief = "flat")

back_button.place(
    x = 950, y = 0,
    width = 50,
    height = 49)

# Login Screen
LoginCanvas = Canvas(
    root,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")
LoginCanvas.place(x=0, y=0)

first_name_img = PhotoImage(file=assets + f"Login_FirstName.png")
first_name_bg = LoginCanvas.create_image(
    727.5, 225.5,
    image=first_name_img)

first_name = Entry(
    bd=0,
    bg="#e9e9e9",
    highlightthickness=0)

first_name.place(
    x=610.5, y=200,
    width=234.0,
    height=49)

last_name_img = PhotoImage(file=assets + f"Login_SecondName.png")
last_name_bg = LoginCanvas.create_image(
    727.5, 321.5,
    image=last_name_img)

last_name = Entry(
    bd=0,
    bg="#e9e9e9",
    highlightthickness=0)

last_name.place(
    x=610.5, y=296,
    width=234.0,
    height=49)

get_started_img = PhotoImage(file=assets + f"Login_GetStarted.png")
get_started = Button(
    image=get_started_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: GetStarted(WelcomeCanvas, test_recognition,
                               face_recognition, logout, backup, first_name, last_name, get_started, storage, LOCAL_USER_IDS, CLOUD_USER_IDS),
    relief="flat")

get_started.place(
    x=647, y=399,
    width=153,
    height=49)

Welcome_background_image = PhotoImage(file=assets + f"Welcome_Background.png")
background = WelcomeCanvas.create_image(
    416.5, 300.0,
    image=Welcome_background_image)

Login_background_image = PhotoImage(file=assets + f"Login_Background.png")
background = LoginCanvas.create_image(
    508.5, 300.0,
    image=Login_background_image)


Webcam_background_image = PhotoImage(file=assets + f"WebcamBackground.png")
background = WebcamCanvas.create_image(
    500.0, 300.0,
    image=Webcam_background_image)

# Cloud Storage
firebase = pyrebase.initialize_app(firebase_config)

storage = firebase.storage()
root.resizable(False, False) # Stops users changing resolution of GUI

if __name__ == "__main__":
    root.mainloop()
