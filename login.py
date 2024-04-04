from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import ttk
from tkinter.ttk import *
import tkinter as tk 
from tkinter import *
import mysql.connector
from tkinter import messagebox
import sys
from main import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\warre\Downloads\python\build\assets\frame0")

def login():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="library")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return
    else:
        print("Connection established successfully")
        print("Enter your username and password")
        
        userid = User.get()
        passw = Pass.get()
        
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM user WHERE username = %s AND password = %s", (userid, passw))
        
        myresult = cur.fetchone()
        
        print(myresult)
        
    #checking
        
    if len(userid) == 0 and len(passw) == 0:
        messagebox.showinfo("Login Failed", "Please fill up username and password")
    elif len(userid) == 0:
        messagebox.showinfo("Login Failed", "Username Empty")
    elif len(passw) == 0:
        messagebox.showinfo("Login Failed", "Password Empty")
    else:
        if myresult:
            if myresult[3] == 1:
                messagebox.showinfo("Login Successful", "Welcome, Admin!")
                obj.withdraw()
                app = Library()

            elif myresult[3] == 0:
                messagebox.showinfo("Login Successful", "Welcome, user!")
            else:
                messagebox.showinfo("Login Failed", "Invalid User!")
        else:
            messagebox.showinfo("Login Failed", "Incorrect username/password")
            
        cur.close()
        conn.close()
    
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def home():
    # Write your home screen code here
    pass

obj = Tk()
obj.geometry("475x350")
obj.configure(bg="LightSkyBlue")

canvas = Canvas(
    obj,
    bg="LightSkyBlue",
    height=350,
    width=475,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_text(
    40.0,
    23.0,
    anchor="nw",
    text="Library Managment System",
    fill="#FFFFFF",
    font=("Inter Bold", 30 * -1)
)

canvas.create_text(
    59.0,
    110.0,
    anchor="nw",
    text="Username:",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)
canvas.create_text(
    63.0,
    178.0,
    anchor="nw",
    text="Password:",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    230.0,
    153.0,
    image=entry_image_1
)
User = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0

)
User.place(
    x=62.0,
    y=138.0,
    width=336.0,
    height=28.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    231.0,
    221.0,
    image=entry_image_2
)
Pass = Entry(
    show='*',
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
Pass.place(
    x=63.0,
    y=206.0,
    width=336.0,
    height=28.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=login,
    relief="flat"
)
button_1.place(
    x=288.0,
    y=264.0,
    width=110.0,
    height=38.0
)
obj.resizable(False, False)

obj.mainloop()

