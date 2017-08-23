import tkinter as tk
from wifi.WifiGui import WifiSelectionWindow

class MainWindow:
    def __init__(self):
        # Fenêtre vide
        self.root = tk.Tk()
        # Obliger le plein écran
        #self.root.attributes('-fullscreen', True)
        # Frame
        self.frame = tk.Frame(self.root)

        self.b = tk.Button(self.frame, text="Changer de réseau Wi-Fi", command=self.launchWSW, font=("Helvetica", 20))
        self.b.pack()

        # Packing des élements
        self.frame.pack()

        # Lancement de la boucle du programme
        self.root.mainloop()

    def launchWSW(self):
        WSW = WifiSelectionWindow()

MW = MainWindow()
