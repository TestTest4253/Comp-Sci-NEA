import os
import sys
import subprocess

try:
    import tkinter
except ImportError:
    devnull = open(os.devnull, "w")
    print("Installing tkinter")
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "tkinter"], stdout=devnull, stderr=devnull)

try:
    import pyrebase
except ImportError:
    # os.devnull is the null file for windows
    devnull = open(os.devnull, "w")
    print("Installing pyrebase")
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "pyrebase4"], stdout=devnull, stderr=devnull)

try:
    import cv2
except ImportError:
    devnull = open(os.devnull, "w")
    print("Installing open-cv")
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "opencv-contrib-python"], stdout=devnull, stderr=devnull)

try:
    import PIL
except ImportError:
    devnull = open(os.devnull, "w")
    print("Installing pillow")
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "pillow"], stdout=devnull, stderr=devnull)

try:
    import matplotlib
except ImportError:
    devnull = open(os.devnull, "w")
    print("Installing matplotlib")
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "matplotlib"], stdout=devnull, stderr=devnull)

print("All modules installed, you may now run the original code")
