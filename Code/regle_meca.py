# regle_meca.py / Tom

import json
import random
from pathlib import Path

# Variables globales pour le jeu
NOMBRE_CARTES_DEBUT = 7
POINTS_UNO = 50
POINTS_SPECIAL = 20

class Carte:
    """Classe pour représenter une carte UNO"""
    def __init__(self, id_carte, donnees):
        self.id = id_carte
        self.couleur = donnees.get("card.color", "none")
        self.valeur = donnees.get("card.value", "0")
        self.sprite = donnees.get("card.sprite", "")
        self.type = donnees.get("card.type", "basic")
        
        # Pour vérifier si c'est une carte noire (joker ou +4)
        self.est_noire = self.couleur in ["none", "noir", "noire"]
    
    def __str__(self):
        return f"{self.valeur} {self.couleur}"
    
    def __repr__(self):
        return f"Carte({self.id}, {self.valeur}, {self.couleur})"

class MoteurJeu:
    """Moteur principal du jeu UNO"""
    
    def __init__(self, fichier_cartes="card.json", fichier_config="constants.json"):
        print("Initialisation du moteur de jeu UNO...")
        
        # Attributs du jeu
        self.carte_visible = None
        self.couleur_actuelle = None
        self.sens_horaire = True
        self.joueur_actuel = 0
        self.cartes_jeu = []
        self.config = {}
        self.sauvegardes = {}
        
        # Charger les fichiers
        try:
            self.charger_cartes(fichier_cartes)
            self.charger_config(fichier_config)
            print("Fichiers chargés avec succès")
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
    
    def charger_cartes(self, nom_fichier):
        """Charge les cartes depuis le fichier JSON"""
        chemin = Path(nom_fichier)
        
        if not chemin.exists():
            raise FileNotFoundError(f"Le fichier {nom_fichier} n'existe pas")
        
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Créer les objets Carte
        self.cartes_jeu = []
        for carte_dict in data.get("card", []):
            for id_carte, donnees in carte_dict.items():
                self.cartes_jeu.append(Carte(id_carte, donnees))
        
        print(f"{len(self.cartes_jeu)} cartes chargées")
    
    def charger_config(self, nom_fichier):
        """Charge la configuration depuis le fichier JSON"""
        chemin = Path(nom_fichier)
        
        if not chemin.exists():
            raise FileNotFoundError(f"Le fichier {nom_fichier} n'existe pas")
        
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.config = data.get("settings", [{}])[0]
        self.sauvegardes = data.get("files.save", {})
        
        print("Configuration chargée")
    
    def creer_pioche(self):
        """Crée une pioche mélangée"""
        pioche = self.cartes_jeu.copy()
        random.shuffle(pioche)
        return pioche
    
    def distribuer_cartes(self, nb_joueurs, nb_cartes=NOMBRE_CARTES_DEBUT):
        """Distribue les cartes aux joueurs"""
        pioche = self.creer_pioche()
        mains = []
        
        for i in range(nb_joueurs):
            main = pioche[:nb_cartes]
            pioche = pioche[nb_cartes:]
            mains.append(main)
        
        return mains, pioche
    
    def peut_jouer(self, carte):
        """Vérifie si une carte peut être jouée"""
        # Les jokers peuvent toujours être joués
        if carte.valeur in ["joker", "+4"]:
            return True
        
        # Même couleur
        if self.couleur_actuelle and carte.couleur == self.couleur_actuelle:
            return True
        
        # Même valeur
        if self.carte_visible and carte.valeur == self.carte_visible.valeur:
            return True
        
        return False
    
    def verifier_plus4(self, main_joueur):
        """Vérifie si le joueur peut jouer un +4"""
        if not self.couleur_actuelle:
            return True
        
        for carte in main_joueur:
            if carte.couleur == self.couleur_actuelle:
                return False  # Il a une carte de la bonne couleur
        
        return True  # Il peut jouer le +4
    
    def jouer_carte(self, carte, main_joueur, couleur_choisie=None):
        """Joue une carte et met à jour l'état du jeu"""
        if not self.peut_jouer(carte):
            return False, "Cette carte ne peut pas être jouée !"
        
        # Vérifier le +4
        if carte.valeur == "+4" and not self.verifier_plus4(main_joueur):
            return False, "Vous ne pouvez pas jouer +4 si vous avez une carte de la couleur actuelle !"
        
        # Mettre à jour la carte visible
        self.carte_visible = carte
        
        # Mettre à jour la couleur
        if carte.couleur not in ["none", "noir", "noire"]:
            self.couleur_actuelle = carte.couleur
        elif couleur_choisie:
            self.couleur_actuelle = couleur_choisie
        
        return True, "Carte jouée avec succès !"
    
    def appliquer_effet(self, carte, nb_joueurs):
        """Applique l'effet d'une carte spéciale"""
        effet = {
            "piocher": 0,
            "sauter": False,
            "inverse": False
        }
        
        if carte.valeur == "+2":
            effet["piocher"] = 2
            effet["sauter"] = True
        
        elif carte.valeur == "inverse":
            self.sens_horaire = not self.sens_horaire
            effet["inverse"] = True
            # Si 2 joueurs, ça équivaut à passer son tour
            if nb_joueurs == 2:
                effet["sauter"] = True
        
        elif carte.valeur == "passe":
            effet["sauter"] = True
        
        elif carte.valeur == "+4":
            effet["piocher"] = 4
            effet["sauter"] = True
        
        return effet
    
    def joueur_suivant(self, nb_joueurs):
        """Passe au joueur suivant"""
        if self.sens_horaire:
            self.joueur_actuel = (self.joueur_actuel + 1) % nb_joueurs
        else:
            self.joueur_actuel = (self.joueur_actuel - 1) % nb_joueurs
        
        return self.joueur_actuel
    
    def sauter_joueur(self, nb_joueurs):
        """Saute le joueur suivant (pour +2, passe, +4)"""
        self.joueur_suivant(nb_joueurs)
        self.joueur_suivant(nb_joueurs)
        return self.joueur_actuel
    
    def gerer_premiere_carte(self, premiere_carte, donneur):
        """Gère la première carte retournée"""
        self.carte_visible = premiere_carte
        
        # Cas spécial : +4 au début (interdit)
        if premiere_carte.valeur == "+4":
            return None, "remettre"
        
        # Cas +2
        if premiere_carte.valeur == "+2":
            self.couleur_actuelle = premiere_carte.couleur
            premier = (donneur + 1) % 4
            return premier, {"piocher": 2, "sauter": True}
        
        # Cas inverse
        if premiere_carte.valeur == "inverse":
            self.couleur_actuelle = premiere_carte.couleur
            self.sens_horaire = not self.sens_horaire
            return donneur, None
        
        # Cas passe
        if premiere_carte.valeur == "passe":
            self.couleur_actuelle = premiere_carte.couleur
            premier = (donneur + 1) % 4
            suivant = (premier + 1) % 4
            return suivant, None
        
        # Cas joker
        if premiere_carte.valeur == "joker":
            premier = (donneur + 1) % 4
            return premier, "choisir_couleur"
        
        # Carte normale
        self.couleur_actuelle = premiere_carte.couleur
        premier = (donneur + 1) % 4
        return premier, None
    
    def verifier_uno(self, nb_cartes, a_dit_uno):
        """Vérifie si le joueur a dit UNO"""
        if nb_cartes == 1 and not a_dit_uno:
            return 2  # Pénalité de 2 cartes
        return 0
    
    def calculer_points(self, main):
        """Calcule les points d'une main"""
        total = 0
        for carte in main:
            if isinstance(carte.valeur, int):
                total += carte.valeur
            elif carte.valeur in ["+2", "inverse", "passe"]:
                total += POINTS_SPECIAL
            elif carte.valeur in ["joker", "+4"]:
                total += POINTS_UNO
        return total
    
    def partie_finie(self, nb_cartes):
        """Vérifie si la partie est terminée"""
        return nb_cartes == 0
    
    def sauvegarder_partie(self, nom_sauvegarde, etat_jeu):
        """Sauvegarde l'état de la partie"""
        if nom_sauvegarde not in self.sauvegardes:
            print(f"Sauvegarde '{nom_sauvegarde}' non trouvée dans la configuration")
            return False
        
        try:
            with open(self.sauvegardes[nom_sauvegarde], "w") as f:
                json.dump(etat_jeu, f, indent=2)
            print(f"Partie sauvegardée dans {nom_sauvegarde}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False
    
    def charger_partie(self, nom_sauvegarde):
        """Charge une partie sauvegardée"""
        if nom_sauvegarde not in self.sauvegardes:
            print(f"Sauvegarde '{nom_sauvegarde}' non trouvée")
            return None
        
        try:
            with open(self.sauvegardes[nom_sauvegarde], "r") as f:
                etat = json.load(f)
            print(f"Partie chargée depuis {nom_sauvegarde}")
            return etat
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            return None

# Exemple d'utilisation du moteur
if __name__ == "__main__":
    print("=== Test du moteur de jeu UNO ===")
    
    # Créer le moteur
    jeu = MoteurJeu()
    
    # Distribuer les cartes
    mains, pioche = jeu.distribuer_cartes(4)
    
    print(f"Cartes distribuées : {len(mains)} joueurs")
    for i, main in enumerate(mains):
        print(f"Joueur {i+1} : {len(main)} cartes")
    
    # Afficher quelques cartes
    print("Exemple de cartes :")
    for i in range(min(5, len(jeu.cartes_jeu))):
        print(f"  - {jeu.cartes_jeu[i]}")
    
    print("Moteur de jeu prêt !")
