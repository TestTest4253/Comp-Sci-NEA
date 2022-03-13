import os
import pyrebase
import time

firebase_config = {"apiKey": "AIzaSyDbs8Yl971Tqhu4VRXHn3kpRhORmUIk-oo",
                   "authDomain": "computer-science-nea-8f6be.firebaseapp.com",
                   "projectId": "computer-science-nea-8f6be",
                   "storageBucket": "computer-science-nea-8f6be.appspot.com",
                   "messagingSenderId": "231523471417",
                   "appId": "1:231523471417:web:2fd16b7b8003693e0f7de8",
                   "measurementId": "G-9TGMPRHP0R",
                   "databaseURL": "https://computer-science-nea-8f6be.firebaseio.com"}

# Paths


firebase = pyrebase.initialize_app(firebase_config)

storage = firebase.storage()

faces_dir = "FacialRecognition/Faces"

folders = os.listdir(faces_dir)
for folder in folders:
    try:
        storage.child(f"Faces/{folder}/myimage1.png").download(
            f"Faces/{folder}/myimage1.png", "Downloaded.txt")
        os.remove("Downloaded.txt")
        print(f"{folder} exists")
    except:
        for image in os.listdir(faces_dir+"\\"+folder):
            cloud_path = f"Faces/{folder}/{image}"
            local_path = faces_dir+"\\"+folder+"\\"+image
            storage.child(cloud_path).put(local_path)
            print(f"Uploading {image}")
            time.sleep(0.15)
