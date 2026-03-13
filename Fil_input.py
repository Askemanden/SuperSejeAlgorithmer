from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json

def skid() -> dict:
    Tk().withdraw()  # skjul tkinter-vinduet

    filnavn = askopenfilename(
        title="Vælg en JSON-fil",
        filetypes=[("JSON filer", "*.json"), ("Alle filer", "*.*")]
    )

    if filnavn:
        with open(filnavn, "r", encoding="utf-8") as f:
            data = json.load(f)
            print("Indlæst JSON:", data)
            return data
    else:
        data = {}
        print("Du er en abe")
        return data