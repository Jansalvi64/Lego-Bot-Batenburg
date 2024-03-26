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
    x_offset = 20
    y_offset = 30
    nop_afstand = 20  # Afstand tussen nopjes
    nop_diameter = 10  # Diameter van de nopjes
    max_breedte = 0
    for naam, blokje in blokjes.items():
        lengte = blokje.get("breedte", 0)
        breedte = blokje.get("lengte", 0)
        hoogte = blokje.get("hoogte", 0)
        max_breedte = max(max_breedte, breedte)
        canvas.create_text(x_offset + lengte * nop_afstand / 2, y_offset - 10, text=naam)  # Weergeven van de naam van het blokje boven het blokje
        canvas.create_rectangle(x_offset, y_offset, x_offset + lengte * nop_afstand, y_offset + breedte * nop_afstand, fill="yellow")  # Tekenen van het LEGO-blokje
        for x in range(lengte):
            for y in range(breedte):
                nop_x = x_offset + x * nop_afstand + nop_afstand / 2
                nop_y = y_offset + y * nop_afstand + nop_afstand / 2
                canvas.create_oval(nop_x - nop_diameter / 2, nop_y - nop_diameter / 2, nop_x + nop_diameter / 2, nop_y + nop_diameter / 2, fill="black", outline="black")  # Zwart cirkel voor een nopje
        
        x_offset += (lengte * nop_afstand) + 40  # Extra ruimte tussen de blokjes
        if x_offset > 80:  # Nieuwe regel beginnen als het canvas vol raakt
            x_offset = 20
            y_offset += max_breedte * nop_afstand + 30  # Extra ruimte tussen de regels
            max_breedte = 0  # Reset de maximale breedte voor de volgende regel

def laad_json_bestand(bestandsnaam):
    with open(bestandsnaam, 'r') as f:
        try:
            data = json.load(f)
            toon_lego_blokjes(data)
        except json.JSONDecodeError:
            messagebox.showerror("Fout", "Ongeldig JSON-formaat")

def voeg_blokje_toe(naam, lengte, breedte, hoogte):
    try:
        with open("blokjes.json", 'r+') as f:
            data = json.load(f)
            nieuw_blokje = {"lengte": int(lengte), "breedte": int(breedte), "hoogte": int(hoogte)}
            data[naam] = nieuw_blokje
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()  # Zorg ervoor dat het bestand wordt bijgewerkt voordat we het opnieuw laden
            messagebox.showinfo("Succes", f"Nieuw LEGO blokje '{naam}' toegevoegd!")
            laad_json_bestand("blokjes.json")  # Laad het JSON-bestand opnieuw om het nieuwe blokje weer te geven
    except (json.JSONDecodeError, ValueError):
        messagebox.showerror("Fout", "Ongeldige invoer voor lengte, breedte of hoogte!")

def verwijder_blokje(naam):
    try:
        with open("blokjes.json", 'r+') as f:
            data = json.load(f)
            if naam in data:
                del data[naam]
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()  # Zorg ervoor dat het bestand wordt bijgewerkt voordat we het opnieuw laden
                messagebox.showinfo("Succes", f"Blokje '{naam}' verwijderd uit blokjes.json!")
                laad_json_bestand("blokjes.json")  # Laad het JSON-bestand opnieuw om het verwijderde blokje niet meer weer te geven
            else:
                messagebox.showerror("Fout", f"Blokje '{naam}' niet gevonden in blokjes.json!")
    except (json.JSONDecodeError, ValueError):
        messagebox.showerror("Fout", "Er is een fout opgetreden bij het verwijderen van het blokje!")


root = tk.Tk()
root.title("LEGO Blokje Viewer")

left_frame = ttk.Frame(root)
left_frame.pack(padx=10, pady=10, side ="left")

bediening_frame = ttk.Frame(left_frame)
bediening_frame.pack(padx=10, pady=10)

blokjes_frame = Frame(left_frame, bg="white")
blokjes_frame.pack(padx=10, pady=10)

canvas = tk.Canvas(blokjes_frame, width=200, height=800, bg="white")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(blokjes_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

# Voeg invoervelden toe voor het toevoegen van een nieuw blokje
naam_label = ttk.Label(bediening_frame, text="Naam:")
naam_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
naam_entry = ttk.Entry(bediening_frame)
naam_entry.grid(row=0, column=1, padx=5, pady=5)

lengte_label = ttk.Label(bediening_frame, text="Lengte:")
lengte_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
lengte_entry = ttk.Entry(bediening_frame)
lengte_entry.grid(row=1, column=1, padx=5, pady=5)

breedte_label = ttk.Label(bediening_frame, text="Breedte:")
breedte_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
breedte_entry = ttk.Entry(bediening_frame)
breedte_entry.grid(row=2, column=1, padx=5, pady=5)

hoogte_label = ttk.Label(bediening_frame, text="Hoogte:")
hoogte_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
hoogte_entry = ttk.Entry(bediening_frame)
hoogte_entry.grid(row=3, column=1, padx=5, pady=5)

toevoegen_knop = ttk.Button(bediening_frame, text="Voeg blokje toe", command=lambda: voeg_blokje_toe(naam_entry.get(), lengte_entry.get(), breedte_entry.get(), hoogte_entry.get()))
toevoegen_knop.grid(row=4, columnspan=2, padx=5, pady=5)

verwijderen_knop = ttk.Button(bediening_frame, text="Verwijder blokje", command=lambda: verwijder_blokje(naam_entry.get()))
verwijderen_knop.grid(row=5, columnspan=2, padx=5, pady=5)

laad_json_bestand("blokjes.json")

root.mainloop()