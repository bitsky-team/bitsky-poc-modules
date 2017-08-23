#!/usr/bin/python3
# coding: utf-8

import os, re

# Module Wi-Fi
# Gère la connexion au réseau Wi-Fi
class WM:
    def getSSIDlist(self):
        results = os.popen('sudo iw dev wlan0 scan | grep SSID').read() # On stocke la chaîne de caractères dans une variable
        results = results.split('\n') # On transforme cette chaîne de caractère en liste
        results = list(set(results)) # On enlève les doublons
        ssids = list() # On crée une liste qui va contenir les SSIDs

        if results:
            for result in results:
                ssid = result.replace("\\x00", "") # On enlève les caractères hexadécimaux
                ssid = ssid[7:] # On enlève la partie "SSID: "
                if ssid: # Si la ligne n'est pas vide
                    ssids.append(ssid) # On l'ajoute dans notre liste de SSIDs

        if ssids: # Si la liste n'est pas vide
            return ssids # On retourne la liste
        else:
            return None # Sinon on retourne None
