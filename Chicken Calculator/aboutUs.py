import tkinter as tk
from tkinter import *

root = tk.Tk()

root.geometry("1000x100")
root.title("About Us")

frame = tk.Frame(root)
frame.grid(row=0, column=0)

Grid.rowconfigure(root,0,weight=1)
Grid.columnconfigure(root,0,weight=1)

title = tk.Label(frame, text="What is this?")
title.grid(row=1, columnspan=7, column=0, sticky="NSEW")

text = tk.Label(frame, text="This tool is a calculator that shows how many chickens you have ever eaten, simply input your age in the box and one you submit it, it will show you how many chickens you have ever eaten.")
text.grid(row=2, columnspan=7, column=0, sticky="NSEW")

text2 = tk.Label(frame, text="This calculator is arithmetic and does not take into account religion or food preference.")
text2.grid(row=3, columnspan=7,  column=0, sticky="NSEW")

root.mainloop()
