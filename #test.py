import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import StringVar
from tkinter import colorchooser
from tkinter import messagebox
import csv
import json

def toon_lego_blokjes(blokjes):
    canvas.delete("all")  # Wis het canvas
    x_offset = 10
    y_offset = 10
    for naam, blokje in blokjes.items():
        lengte = blokje.get("breedte", 0)
        breedte = blokje.get("lengte", 0)
        hoogte = blokje.get("hoogte", 0)
        canvas.create_rectangle(x_offset, y_offset, x_offset + lengte * 20, y_offset + breedte * 20, fill="yellow")  # Tekenen van het LEGO-blokje
        canvas.create_text(x_offset + lengte * 10, y_offset + breedte * 10, text=naam)  # Weergeven van de naam van het blokje
        x_offset += (lengte * 20) + 20
        if x_offset > 80:  # Nieuwe regel beginnen als het canvas vol raakt. waarde is de breedte van canvas
            x_offset = 10
            y_offset += (lengte * 50)+20

def laad_json_bestand():
    bestandsnaam = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if bestandsnaam:
        with open(bestandsnaam, 'r') as f:
            try:
                data = json.load(f)
                toon_lego_blokjes(data)
            except json.JSONDecodeError:
                messagebox.showerror("Fout", "Ongeldig JSON-formaat")

root = tk.Tk()
root.title("LEGO Blokje Viewer")

bediening_frame = ttk.Frame(root)
bediening_frame.pack(padx=10, pady=10)

laad_knop = ttk.Button(bediening_frame, text="Laad JSON", command=laad_json_bestand)
laad_knop.pack(side=tk.LEFT, padx=5)

canvas = tk.Canvas(root, width=600, height=400, bg="white")
canvas.pack(padx=10, pady=10)

root.mainloop()