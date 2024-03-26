import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import StringVar
from tkinter import colorchooser
from tkinter import messagebox
import csv
import json

root = tk.Tk()
root.title("BE Precision Technology - Probe Card Tester")
root.geometry(f"{1920}x{1080}")  # Set the initial window size to 1920x1080 pixels
root.configure(bg="white")

# Create A Main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

root.mainloop()