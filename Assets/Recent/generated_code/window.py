from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("1000x600")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=600,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(
    file=f"Assets/Recent/generated_code/background.png")
background = canvas.create_image(
    499.5, 232.0,
    image=background_img)

img0 = PhotoImage(file=f"Assets/Recent/generated_code/img0.png")
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=btn_clicked,
    relief="flat")

b0.place(
    x=442, y=508,
    width=116,
    height=49)

window.resizable(False, False)
window.mainloop()
