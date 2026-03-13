from tkinter import Tk
from tkinter.filedialog import askopenfilename
import json
from  jsongraph import *

def skid() ->Tuple[Graph,int] :
    Tk().withdraw()  # skjul tkinter-vinduet

    filnavn = askopenfilename(
        title="Vælg en JSON-fil",
        filetypes=[("JSON filer", "*.json"), ("Alle filer", "*.*")]
    )

    if filnavn:
        return readData(filnavn)
    else:
        data : Tuple[Graph,int] = ([(0,1,1)],2)
        print("Du er en abe")
        return data