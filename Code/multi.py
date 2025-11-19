# Coder toutes les classes\methodes liées au multijoueurs
from Gestion_Cartes import *

import random

class Carte:
    def __init__(self, couleur, valeur):
        self.couleur = couleur   # 'rouge', 'jaune', 'vert', 'bleu' ou 'noir' (joker)
        self.valeur = valeur     # 0-9, 'inverse', 'passe', '+2', 'joker', '+4'

    def __repr__(self):
        return f"{self.couleur} {self.valeur}"


class JeuDeCartes:
    def __init__(self):
        self.cartes = self.creer_jeu()

    def creer_jeu(self):
        couleurs = ['rouge', 'jaune', 'vert', 'bleu']
        valeurs = list(range(10)) + ['inverse', 'passe', '+2']
        jeu = []

        # Cartes de couleur
        for couleur in couleurs:
            for valeur in valeurs:
                jeu.append(Carte(couleur, valeur))
                if valeur != 0:
                    jeu.append(Carte(couleur, valeur))  # deux exemplaires sauf 0

        # Jokers
        for _ in range(4):
            jeu.append(Carte('noir', 'joker'))
            jeu.append(Carte('noir', '+4'))

        random.shuffle(jeu)
        return jeu

    def piocher(self, n=1):
        cartes_piochees = self.cartes[:n]
        self.cartes = self.cartes[n:]
        return cartes_piochees


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.cartes = []

    def piocher_carte(self, carte):
        self.cartes.append(carte)

    def jouer_carte(self, index):
        carte_jouee = self.cartes[index]
        self.cartes.pop(index)
        return carte_jouee
        


class Game:
    def __init__(self, liste_joueurs):
        self.liste_joueurs = liste_joueurs
        self.joueur_actuel = 0
        self.sens_du_jeu = 1

    def commencer_partie(self, paquet):
        for joueurs in self.liste_joueurs:
            carte_piochees = paquet.piocher(7)
            joueurs.cartes.append(carte_piochees)
        
            

    def tour_suivant(self):
        self.joueur_actuel + 1

    def inverser_sens(self):
        self.liste_joueurs

    def sauter_joueur(self):
        self.joueur_actuel + 1

    def obtenir_joueur_actuel(self):
        joueur_actuel = self.joueur_actuel
        return joueur_actuel


