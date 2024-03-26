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
    y_offset = 20
    nop_afstand = 20  # Afstand tussen nopjes
    nop_diameter = 10  # Diameter van de nopjes
    for naam, blokje in blokjes.items():
        lengte = blokje.get("lengte", 0)
        breedte = blokje.get("breedte", 0)
        hoogte = blokje.get("hoogte", 0)
        canvas.create_text(x_offset + lengte * nop_afstand / 2, y_offset - 10, text=naam)  # Weergeven van de naam van het blokje boven het blokje
        canvas.create_rectangle(x_offset, y_offset, x_offset + lengte * nop_afstand, y_offset + breedte * nop_afstand, fill="yellow")  # Tekenen van het LEGO-blokje
        for x in range(lengte):
            for y in range(breedte):
                nop_x = x_offset + x * nop_afstand + nop_afstand / 2
                nop_y = y_offset + y * nop_afstand + nop_afstand / 2
                canvas.create_oval(nop_x - nop_diameter / 2, nop_y - nop_diameter / 2, nop_x + nop_diameter / 2, nop_y + nop_diameter / 2, fill="black", outline="black")  # Zwart cirkel voor een nopje
        
        x_offset += (lengte * nop_afstand) + 40  # Extra ruimte tussen de blokjes
        if x_offset > 80:  # Nieuwe regel beginnen als het canvas vol raakt
            x_offset = 10
            y_offset += 80  # Extra ruimte tussen de regels

def laad_json_bestand(bestandsnaam):
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

canvas = tk.Canvas(root, width=100, height=400, bg="white")
canvas.pack(padx=10, pady=10)

laad_json_bestand("blokjes.json")

root.mainloop()