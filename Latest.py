from helper import local_binary_pattern, euclidean_distance, User_IDs, hist, backup_files

import os
import urllib
from tkinter import *
import tkinter as tk
import pyrebase
import cv2
import time
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
path_of_gui = "Assets/"
LOCAL_USER_IDS = "tmp/UserIDs.txt"
CLOUD_USER_IDS = "Credentials/UserIDs.txt"
FACES_DIRECTORY = "FacialRecognition/Faces"

# Functions

def GetStarted(canvas, test_recognition,
               face_recognition, logout, backup, first_name, last_name, get_started, storage, LOCAL_USER_IDS, CLOUD_USER_IDS):
    if DEBUG:
        print("Getting Started")
    if first_name.get() and last_name.get() != "":
        first_name = first_name.get().capitalize()
        last_name = last_name.get().capitalize()
        full_name = first_name + " " + last_name
        User_IDs(first_name, last_name,
                 storage, LOCAL_USER_IDS, CLOUD_USER_IDS)
        tk.Misc.lift(canvas, aboveThis=None)
        test_recognition.lift()
        try:
            storage.child(f"Faces/{full_name}/myimage1.png").download(
                f"Faces/{full_name}/myimage1.png", "tmp/downloaded.txt")
            os.remove("tmp/downloaded.txt")
        except:
            face_recognition.lift()
        logout.lift()
        backup.lift()
        first_name.lower()
        last_name.lower()
        get_started.lower()

def log_out(canvas2, test_recognition,
            face_recognition, logout, backup, first_name, last_name, get_started, faces_dir):
    if DEBUG:
        print("Logging out")
    tk.Misc.lift(canvas2, aboveThis=None)
    test_recognition.lower()
    face_recognition.lower()
    logout.lower()
    backup.lower()
    first_name.lift()
    last_name.lift()
    get_started.lift()

def facial_recognition(canvas3, backup, logout, face_recognition, test_recognition, Start_camera_button, Stop_camera_button):
    tk.Misc.lift(canvas3, aboveThis=None)
    backup.lower()
    logout.lower()
    face_recognition.lower()
    test_recognition.lower()
    Start_camera_button.lift()
    Stop_camera_button.lift()

def add_user(first_name, last_name):
    name = first_name.get().capitalize() + " " + last_name.get().capitalize()
    try:
        os.mkdir(f"FacialRecognition/Faces/{name}")
    except FileExistsError:
        pass

def start_button(videoloop_stop):
    thread = threading.Thread(target = videoLoop, args = (videoloop_stop, )).start()

def stop_button(videoloop_stop):
    videoloop_stop[0] = True

def videoLoop(mirror = False):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)

    while True:
        ret, to_draw = cap.read()
        if mirror == True:
            to_draw = to_draw[:,::-1]
        image = cv2.cvtColor(to_draw, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        tkimage = ImageTk.PhotoImage(image)
        panel = tk.Label(image=tkimage)
        panel.image = tkimage
        panel.place(x=50, y=50)

        if videoloop_stop[0]:
            videoloop_stop[0] = False
            image.save("Swag.png")
            panel.destroy()
            break

videoloop_stop = [False]
# GUI Creation
root = Tk()

root.geometry("1000x600")
root.configure(bg="#ffffff")

# Welcome Screen
canvas = Canvas(
    root,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

face_recognition_img = PhotoImage(file=path_of_gui + f"Welcome_Face.png")
face_recognition = Button(
    image=face_recognition_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: add_user(first_name, last_name),
    relief="flat")

face_recognition.place(
    x=555, y=198,
    width=339,
    height=53)

test_recognition_img = PhotoImage(file=path_of_gui + f"Welcome_Test.png")
test_recognition = Button(
    image=test_recognition_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: facial_recognition(canvas3, backup, logout, face_recognition, test_recognition, Start_camera_button, Stop_camera_button),
    relief="flat")

test_recognition.place(
    x=556, y=293,
    width=339,
    height=53)

logout_img = PhotoImage(file=path_of_gui + f"Welcome_Logout.png")
logout = Button(
    image=logout_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: log_out(canvas2, test_recognition,
                            face_recognition, logout, backup, first_name, last_name, get_started, FACES_DIRECTORY),
    relief="flat")

logout.place(
    x=662, y=395,
    width=126,
    height=53)

backup_img = PhotoImage(file=path_of_gui + f"Welcome_info.png")
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

canvas3 = Canvas(
    root,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")

webcam_background_img = PhotoImage(file = path_of_gui+f"Webcambackground.png")
background = canvas3.create_image(
    500.0, 300.0,
    image=webcam_background_img)

Start_camera_img = PhotoImage(file = path_of_gui+f"StartCamera.png")
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

Stop_camera_img = PhotoImage(file = path_of_gui+f"StopCamera.png")
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

# Login Screen
canvas2 = Canvas(
    root,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas2.place(x=0, y=0)

first_name_img = PhotoImage(file=path_of_gui + f"Login_FirstName.png")
first_name_bg = canvas2.create_image(
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

last_name_img = PhotoImage(file=path_of_gui + f"Login_SecondName.png")
last_name_bg = canvas2.create_image(
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

get_started_img = PhotoImage(file=path_of_gui + f"Login_GetStarted.png")
get_started = Button(
    image=get_started_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: GetStarted(canvas, test_recognition,
                               face_recognition, logout, backup, first_name, last_name, get_started, storage, LOCAL_USER_IDS, CLOUD_USER_IDS),
    relief="flat")

get_started.place(
    x=647, y=399,
    width=153,
    height=49)


background_img2 = PhotoImage(file=path_of_gui + f"Login_Background.png")
background = canvas2.create_image(
    508.5, 300.0,
    image=background_img2)

background_img = PhotoImage(file=path_of_gui + f"Welcome_Background.png")
background = canvas.create_image(
    416.5, 300.0,
    image=background_img)

# Facial Recognition Screen



# Cloud Storage
firebase = pyrebase.initialize_app(firebase_config)

storage = firebase.storage()
root.resizable(False, False)
if __name__ == "__main__":
    root.mainloop()
