import tkinter as tk
from tkinter import *
from tkinter import ttk



root = Tk()

root.title("Shopping List")

#Blue Frame

frame1 = Frame(root, bg="#181818", height=1080, width=1920)

frame1.grid()

#Shopping List Label

title = Label(frame1, text="Shopping List", font="DS-Digital")

title.grid(row=0, column=0, columnspan=4)

#Items Listbox

items = Listbox(frame1)
items.grid(row=1, column=0, columnspan=4)

#Item Entry

itemLabel = Label(frame1, text="Enter Item Below:", font="DS-Digital")
itemLabel.grid(row=2, column=0, columnspan=4)
content = StringVar()

itemEntry = Entry(frame1, textvariable=content)
itemEntry.grid(row=3, column=0, columnspan=4)

#Put Words in list
def add():
    items.insert(END, content.get())
    itemEntry.delete(0, END)

#Take Words out of list
def delete():
    items.delete(ANCHOR)

#Clear List:
def clear():
    items.delete(0, END)

#Useless Buttons

addEntry = Button(frame1, text="Add", command=add, font="DS-Digital")
addEntry.grid(row=4, column=0)

deleteEntry = Button(frame1, text="Delete", command=delete, font="DS-Digital")
deleteEntry.grid(row=4, column=1)

clearList = Button(frame1, text="Clear", command=clear, font="DS-Digital")
clearList.grid(row=4, column=2)

quit = Button(frame1, text="Self-Destruct", command=quit, font="DS-Digital")
quit.grid(row=4, column=3)

root.mainloop()
