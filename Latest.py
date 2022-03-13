from helper import local_binary_pattern, euclidean_distance, User_IDs, hist

import os
import urllib
from tkinter import *
from VideoCapture import Webcam
import pyrebase
import tkinter
import cv2
import time

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
               face_recognition, logout, info, first_name, last_name, get_started, storage, LOCAL_USER_IDS, CLOUD_USER_IDS):
    if DEBUG:
        print("Getting Started")
    if first_name.get() and last_name.get() != "":
        first_name = first_name.get().capitalize()
        last_name = last_name.get().capitalize()
        full_name = first_name + " " + last_name
        User_IDs(first_name, last_name,
                 storage, LOCAL_USER_IDS, CLOUD_USER_IDS)
        tkinter.Misc.lift(canvas, aboveThis=None)
        test_recognition.lift()
        try:
            storage.child(f"Faces/{full_name}/myimage1.png").download(
                f"Faces/{full_name}/myimage1.png", "tmp/downloaded.txt")
            os.remove("tmp/downloaded.txt")
        except:
            face_recognition.lift()
        logout.lift()
        info.lift()
        first_name.lower()
        last_name.lower()
        get_started.lower()


def user_info():
    if DEBUG:
        print("Showing User Profile")


def log_out(canvas2, test_recognition,
            face_recognition, logout, info, first_name, last_name, get_started, faces_dir):
    if DEBUG:
        print("Logging out")
    tkinter.Misc.lift(canvas2, aboveThis=None)
    test_recognition.lower()
    face_recognition.lower()
    logout.lower()
    info.lower()
    first_name.lift()
    last_name.lift()
    get_started.lift()
    #backup_files(storage, faces_dir)


def facial_recognition():
    if DEBUG:
        print("booting camera")
    Webcam(window, cv2.VideoCapture(0, cv2.CAP_DSHOW))


def add_user(first_name, last_name):
    name = first_name.get().capitalize() + " " + last_name.get().capitalize()
    try:
        os.mkdir(f"FacialRecognition/Faces/{name}")
    except FileExistsError:
        pass


def backup_files(storage, directory):
    folders = os.listdir(directory)
    for folder in folders:
        try:
            storage.child(f"Faces/{folder}/myimage1.png").download(
                f"Faces/{folder}/myimage1.png", "Downloaded.txt")
            os.remove("Downloaded.txt")
            if DEBUG:
                print(f"{folder} exists")
        except:
            for image in os.listdir(directory+"\\"+folder):
                cloud_path = f"Faces/{folder}/{image}"
                local_path = directory+"\\"+folder+"\\"+image
                storage.child(cloud_path).put(local_path)
                if DEBUG:
                    print(f"Uploading {image}")
                time.sleep(0.15)


# GUI Creation
window = Tk()

window.geometry("1000x600")
window.configure(bg="#ffffff")

# Welcome Screen
canvas = Canvas(
    window,
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
    command=facial_recognition,
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
                            face_recognition, logout, info, first_name, last_name, get_started, FACES_DIRECTORY),
    relief="flat")

logout.place(
    x=662, y=395,
    width=126,
    height=53)

info_img = PhotoImage(file=path_of_gui + f"Welcome_Info.png")
info = Button(
    image=info_img,
    borderwidth=0,
    highlightthickness=0,
    command=user_info,
    relief="flat")

info.place(
    x=970, y=570,
    width=30,
    height=30)

# Login Screen
canvas2 = Canvas(
    window,
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
                               face_recognition, logout, info, first_name, last_name, get_started, storage, LOCAL_USER_IDS, CLOUD_USER_IDS),
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

# Cloud Storage
firebase = pyrebase.initialize_app(firebase_config)

storage = firebase.storage()
window.resizable(False, False)
if __name__ == "__main__":
    window.mainloop()
