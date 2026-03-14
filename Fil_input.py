from tkinter import Tk
from tkinter.filedialog import askopenfilename
from jsongraph import *
from typing import Tuple

def skid() -> Tuple[Graph, int]:
    root = Tk()
    root.withdraw()  # skjul vinduet

    filnavn = askopenfilename(
        title="Vælg en JSON-fil",
        filetypes=[("JSON filer", "*.json"), ("Alle filer", "*.*")]
    )

    root.destroy()  # <-- vigtigt!

    print(1)
    if filnavn:
        print(readData(filnavn))
        return readData(filnavn)
    else:
        print("Du er en abe")
        return ([(0,1,1)], 2)
