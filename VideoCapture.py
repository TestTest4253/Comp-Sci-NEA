import tkinter as tk
from PIL import Image, ImageTk
import cv2
class Webcam():
    def __init__(self, window, cap): #F
        self.window = window
        self.cap = cap
        self.width = 430
        self.height = 600
        self.interval = 20
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0)
        self.update_image()
    def update_image(self): #F
        self.image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(self.image)
        self.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.window.after(self.interval, self.update_image)
if __name__ == "__main__":
    Root = tk.Tk()
    Webcam(Root, cv2.VideoCapture(0, cv2.CAP_DSHOW))
    Root.mainloop()