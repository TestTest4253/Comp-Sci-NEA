import pyrebase
import urllib
import os

#!Paths
LOCALIDS = "ProtoTypes/UserIDs.txt"
CLOUDSIDS = "Credentials/UserIDs.txt"

FirebaseConfig = {"apiKey": "AIzaSyDbs8Yl971Tqhu4VRXHn3kpRhORmUIk-oo",
                  "authDomain": "computer-science-nea-8f6be.firebaseapp.com",
                  "projectId": "computer-science-nea-8f6be",
                  "storageBucket": "computer-science-nea-8f6be.appspot.com",
                  "messagingSenderId": "231523471417",
                  "appId": "1:231523471417:web:2fd16b7b8003693e0f7de8",
                  "measurementId": "G-9TGMPRHP0R",
                  "databaseURL": "https://computer-science-nea-8f6be.firebaseio.com"}

Firebase = pyrebase.initialize_app(FirebaseConfig)

Storage = Firebase.storage()

# Uploading
"""
File = input("Enter file name: ")
CloudFile = input("Enter name on cloud: ")
Storage.child(CloudFile).put(File)
"""
# Get URL
"""
print(Storage.child(CloudFile).get_url(None))
"""
# Downloading
"""
DownloadLink = input("Enter director to download: ")
Storage.child(DownloadLink).download(DownloadLink,"Downloaded.txt")
"""
# Reading
"""
path = input("Enter path to file: ")
URL = Storage.child(path).get_url(None)
f = urllib.request.urlopen(URL).read()
print(f)
"""
