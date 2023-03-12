import tkinter as tk
from tkinter import *
import os
count = 0


root = tk.Tk()

root.geometry("200x300")
root.title("Chicken Calculator")
root.iconbitmap("Insert icon path here")

frame = tk.Frame(root)
frame.grid(row=0, column=0)

Grid.rowconfigure(root,0,weight=1)
Grid.columnconfigure(root,0,weight=1)

title = tk.Label(frame, text="Chicken Calculator")
title.grid(row=1, columnspan=7, column=0, sticky="NSEW")

listbox = tk.Listbox(frame)
listbox.grid(row=2, columnspan=3, column=0, sticky="NSEW")

header = tk.Label(frame, text="Input your age below:")
header.grid(row=3, columnspan=3, column=0, sticky="NSEW")

entrybox = tk.Entry(frame)
entrybox.grid(row=4, columnspan=3, column=0, sticky="NSEW")


def calculate():
    #pass
    age = 0
    age = float(entrybox.get())
    chickensEaten = age * 33.80
    listbox.insert(count + 1, round(chickensEaten))
    entrybox.delete(0, END)

submitbox = tk.Button(frame, text="Submit", command=calculate)
submitbox.grid(row=5, columnspan=3, column=0, sticky="NSEW")

def openAbout():
    pass
    os.system("C:/Users/alber/OneDrive/Documents/ChickenCalculator/GUI/AboutUs.py")

aboutButton = tk.Button(frame, text="What is this?", command=openAbout)
aboutButton.grid(row=6 , columnspan=3, column=0, sticky="NSEW")



root.mainloop()
