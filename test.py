import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
from tkinter import StringVar
from tkinter import colorchooser
from tkinter import messagebox
import csv
import json


def toon_lego_blokjes(blokjes, kleur):
    canvas_blokjes.delete("all")  # Wis het canvas
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
        canvas_blokjes.create_text(x_offset + lengte * nop_afstand / 2, y_offset - 10, text=naam)  # Weergeven van de naam van het blokje boven het blokje
        canvas_blokjes.create_rectangle(x_offset, y_offset, x_offset + lengte * nop_afstand, y_offset + breedte * nop_afstand, fill=kleur)  # Tekenen van het LEGO-blokje
        for x in range(lengte):
            for y in range(breedte):
                nop_x = x_offset + x * nop_afstand + nop_afstand / 2
                nop_y = y_offset + y * nop_afstand + nop_afstand / 2
                canvas_blokjes.create_oval(nop_x - nop_diameter / 2, nop_y - nop_diameter / 2, nop_x + nop_diameter / 2, nop_y + nop_diameter / 2, fill="black", outline="black")  # Zwart cirkel voor een nopje
        
        x_offset += (lengte * nop_afstand) + 40  # Extra ruimte tussen de blokjes
        if x_offset > 80:  # Nieuwe regel beginnen als het canvas vol raakt
            x_offset = 20
            y_offset += max_breedte * nop_afstand + 30  # Extra ruimte tussen de regels
            max_breedte = 0  # Reset de maximale breedte voor de volgende regel

def laad_json_bestand(bestandsnaam, kleur="Yellow"):
    with open(bestandsnaam, 'r') as f:
        try:
            data = json.load(f)
            toon_lego_blokjes(data, kleur)
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

def verander_kleur(event):
    kleur = kleuren_keuze.get()
    laad_json_bestand("blokjes.json", kleur)

def create_bouwplaat(canvas):
    canvas_width = canvas.winfo_reqwidth()  # Breedte van het canvas
    canvas_height = canvas.winfo_reqheight()  # Hoogte van het canvas
    
    nop_afstand = 20  # Afstand tussen noppen
    nop_diameter = 10  # Diameter van de noppen
    
    # Bereken het aantal noppen in x- en y-richting op basis van de grootte van het canvas
    num_noppen_x = canvas_width // nop_afstand
    num_noppen_y = canvas_height // nop_afstand
    
    # Bereken de offset om de noppen te centreren op het canvas
    x_offset = (canvas_width - (num_noppen_x * nop_afstand)) / 2
    y_offset = (canvas_height - (num_noppen_y * nop_afstand)) / 2
    
    for x in range(num_noppen_x):
        for y in range(num_noppen_y):
            nop_x = x * nop_afstand + x_offset + nop_afstand / 2
            nop_y = y * nop_afstand + y_offset + nop_afstand / 2
            canvas.create_oval(nop_x - nop_diameter / 2, nop_y - nop_diameter / 2, nop_x + nop_diameter / 2, nop_y + nop_diameter / 2, fill="black")

def start_blokje_draggen(event):
    # Bepaal de grootte van het blokje op basis van het geselecteerde blokje in het canvas
    items = canvas_blokjes.find_closest(event.x, event.y)
    x1, y1, x2, y2 = canvas_blokjes.coords(items[0])
    lengte = (x2 - x1) // 20
    breedte = (y2 - y1) // 20
    
    # Maak een nieuw blokje dat overeenkomt met het geselecteerde blokje
    geselecteerde_blokje = kleuren_keuze.get()
    blokje_aan_muis = canvas_blokjes.create_rectangle(event.x, event.y, event.x + lengte * 20, event.y + breedte * 20, fill=geselecteerde_blokje)

    # Teken de nopjes op het blokje aan de muis
    blokje_nopjes = []
    for x in range(int(lengte)):
        for y in range(int(breedte)):
            nop_x = event.x + x * 20 + 20 / 2
            nop_y = event.y + y * 20 + 20 / 2
            nop_id = canvas_blokjes.create_oval(nop_x - 5, nop_y - 5, nop_x + 5, nop_y + 5, fill="black")
            blokje_nopjes.append(nop_id)

    # Bind het nieuwe blokje aan de muispositie
    canvas_blokjes.bind("<B1-Motion>", lambda event, blokje=blokje_aan_muis, lengte=lengte, breedte=breedte, nopjes=blokje_nopjes: beweeg_blokje_aan_muis(event, blokje, lengte, breedte, nopjes))

def beweeg_blokje_aan_muis(event, blokje, lengte, breedte, nopjes):
    # Update de positie van het blokje om het aan de muis te laten kleven
    canvas_blokjes.coords(blokje, event.x, event.y, event.x + lengte * 20, event.y + breedte * 20)

    # Update de positie van de nopjes op het blokje aan de muis
    for i in range(len(nopjes)):
        x = i // breedte
        y = i % breedte
        nop_x = event.x + x * 20 + 20 / 2
        nop_y = event.y + y * 20 + 20 / 2
        canvas_blokjes.coords(nopjes[i], nop_x - 5, nop_y - 5, nop_x + 5, nop_y + 5)


root = tk.Tk()
root.title("LEGO Blokje Viewer")

# Maximaliseer het venster
root.state("zoomed")

main_frame = ttk.Frame(root)
main_frame.pack(padx=10, side="left")

bediening_frame = ttk.Frame(main_frame)
bediening_frame.pack(padx=10, pady=10, side="left")

blokjes_frame = Frame(main_frame, bg="white", height=5000, width=5000)
blokjes_frame.pack(padx=10, pady=10, side="left")

canvas_blokjes = tk.Canvas(blokjes_frame, width=200, height=800, bg="white")

bouwplaat_canvas = tk.Canvas(blokjes_frame, width=960, height=960, bg="white", borderwidth=2, relief="solid")
bouwplaat_canvas.pack(padx=20, pady=10, side="right")

# Teken de bouwplaat met noppen
create_bouwplaat(bouwplaat_canvas)

scrollbar = ttk.Scrollbar(blokjes_frame, orient="vertical", command=canvas_blokjes.yview)
scrollbar.pack(side="left", fill="y")
canvas_blokjes.pack(side="left", fill="both", expand=True)

canvas_blokjes.configure(yscrollcommand=scrollbar.set)

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

kleuren = ["Red", "Green", "Blue", "Yellow", "Orange"]  # Lijst met vooraf ingestelde kleuren

kleuren_keuze = ttk.Combobox(bediening_frame, values=kleuren, state="readonly")
kleuren_keuze.grid(row=6, columnspan=2, padx=5, pady=5)
kleuren_keuze.bind("<<ComboboxSelected>>", verander_kleur)
kleuren_keuze.set("Yellow")

laad_json_bestand("blokjes.json")

# Voeg een binding toe aan het canvas om het slepen van een blokje te starten wanneer erop wordt geklikt in het keuzemenu
canvas_blokjes.bind("<Button-1>", start_blokje_draggen)

# Teken de bouwplaat met noppen
create_bouwplaat(bouwplaat_canvas)

laad_json_bestand("blokjes.json")

root.mainloop()