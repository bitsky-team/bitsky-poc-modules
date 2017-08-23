# Imports
import tkinter as tk
import os, time
from wifi.WifiModule import WM

# Variable globale
password = None # Stockera le mot de passe du réseau

class WifiSelectionWindow:
    def __init__(self):
        # Fenêtre vide
        self.root = tk.Tk()

        # Obliger le plein écran
        self.root.attributes('-fullscreen', True)

        # Frame
        self.frame = tk.Frame(self.root)

        # "Title Label"
        self.installation_label = tk.Label(self.frame, text="Configuration de votre CloudBox", font=("Helvetica", 30))
        self.installation_label.pack()

        # "Choose Wifi Label"
        self.choose_wifi = tk.Label(self.frame, text="Sélectionnez le réseau auquel vous désirez vous connecter:", font=("Helvetica", 20))
        self.choose_wifi.pack()

        # Liste des SSIDs
        wm = WM() # Création d'une instance du module WiFi
        SSIDs = wm.getSSIDlist() # Récupération des SSIDs des réseaux proches
        self.listbox = tk.Listbox(self.frame, font=("Helvetica", 16)) # Création d'une liste qui va accueillir les SSID

        if(SSIDs != None):
            # Si il y a un ou plusieurs réseaux à proximité, on les ajoute à la liste
            for item in SSIDs:
                self.listbox.insert(tk.END, item)
            self.listbox.pack()
        else:
            # Sinon on prévient l'utilisateur
            self.no_ssid_found = tk.Label(self.frame, text="Aucun réseau détecté à proximité.", font=("Helvetica", 20))
            self.no_ssid_found.pack()

        # Bouton de confirmation
        self.b = tk.Button(self.frame, text="Choisir ce réseau", command=self.buttonSelectWifi, font=("Helvetica", 20))
        self.b.pack()

        # Bouton permettant de fermer la fenêtre
        self.b2 = tk.Button(self.frame, text="Quitter", command=self.Exit, font=("Helvetica", 20))
        self.b2.pack()

        # Packing des élements
        self.frame.pack()

        # Binding des touches (temporaire)
        self.root.bind('<Escape>', self.Exit)

        # Lancement de la boucle du programme
        self.root.mainloop()

    # Fonctions servant au key binding et au(x) boutons
    def Exit(self, event = None):
        self.root.destroy()

    # Evenement lors du choix de réseau
    def buttonSelectWifi(self):
        try:
            ssid = self.listbox.get(self.listbox.curselection()) # On récupère le SSID désiré
            inputDialog = WifiPasswordDialog(self.root, ssid) # On demande le mot de passe via une instance de PasswordDialog
            self.root.wait_window(inputDialog.top) # On attend que l'utilisateur confirme sa saisie

            # Configuration du fichier wpa_supplicant.conf où sera stocké les informations réseau
            os.system('sudo wpa_passphrase "' + ssid + '" "' + password + '" >> /etc/wpa_supplicant/wpa_supplicant.conf')
            os.system("sudo wpa_cli reconfigure")
            os.system("sudo service networking restart")

            # On masque la liste des SSIDs et le bouton de confirmation de choix de réseau
            self.listbox.pack_forget()
            self.b.pack_forget()
            self.b2.pack_forget()

            # On prévient l'utilisateur que le système va redémarrer
            self.choose_wifi.config(text= "Le système va redémarrer dans quelques secondes.\nVeuillez ne pas éteindre ou débrancher votre CloudBox.")

            # On appelle la fonction rebootSystem
            self.root.after(1000, self.rebootSystem)
        except:
            print("Aucune sélection possible")

    # Redémarre le système après 10 secondes
    def rebootSystem(self):
        for i in range(10):
            print(i+1)
            time.sleep(1)
        os.system("sudo reboot")

# Fenêtre secondaire permettant d'insérer le mot de passe du réseau
class WifiPasswordDialog:
    def __init__(self, parent, ssid):
        self.ssid = ssid # Récupération et sauvegarde du SSID du réseau choisi

        # Création de la fenêtre
        top = self.top = tk.Toplevel(parent)

        # Obliger le plein écran
        w, h = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
        self.top.overrideredirect(1)
        self.top.geometry("%dx%d+0+0" % (w, h))

        # "Title" Label
        self.installation_label = tk.Label(top, text="Configuration de votre CloudBox", font=("Helvetica", 30))
        self.installation_label.pack()

        # "Password" Label
        self.passwordLabel = tk.Label(top, text='Entrez le mot de passe du réseau "' + str(self.ssid) + '"', font=("Helvetica", 20))
        self.passwordLabel.pack()

        # "Password" EntryBox
        self.passwordEntryBox = tk.Entry(top, show="*", font=("Helvetica", 20))
        self.passwordEntryBox.pack()

        # Bouton de confirmation de fin de saisie
        self.passwordSubmit = tk.Button(top, text='Se connecter', command=self.send, font=("Helvetica", 20))
        self.passwordSubmit.pack()

    # Fonction appelée lors du clic sur le bouton de confirmation de fin de saisie
    def send(self):
        global password

        password = self.passwordEntryBox.get() # On récupère le mot de passe entré

        self.top.withdraw() # On masque la fenêtre
        self.top.destroy() # On détruit la fenêtre
