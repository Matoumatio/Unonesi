# Coder toutes les classes\methodes liées au multijoueurs
import Gestion_Cartes as Gestion_Cartes
from Gestion_Cartes import Carte, JeuDeCartes

import random
"""
class Carte:
    def __init__(self, couleur, valeur):
        self.couleur = couleur   # 'rouge', 'jaune', 'vert', 'bleu' ou 'noir' (joker)
        self.valeur = valeur     # 0-9, 'inverse', 'passe', '+2', 'joker', '+4'

    def __repr__(self):
        return f"{self.couleur} {self.valeur}"
"""
"""
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
            jeu.append(Gestion_Cartes(Carte('noir', 'joker')))
            jeu.append(Carte('noir', '+4'))

        random.shuffle(jeu)
        return jeu

    def piocher(self, n=1):
        cartes_piochees = self.cartes[:n]
        self.cartes = self.cartes[n:]
        return cartes_piochees

"""



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
            for carte in carte_piochees:
                joueurs.piocher_carte(carte)


        
    def tour_suivant(self):
        if self.joueur_actuel == len(self.liste_joueurs):
            self.joueur_actuel = 0
        else:
            self.joueur_actuel =+ 1

    def inverser_sens(self):
        self.sens_du_jeu = 1 if self.sens_du_jeu == -1 else -1

    def sauter_joueur(self):
        self.tour_suivant(self)
        self.tour_suivant(self)

    def obtenir_joueur_actuel(self):
        return self.liste_joueurs[self.joueur_actuel]


# TEST
if __name__ == "__main__":
    # Créer des joueurs
    joueur1 = Joueur("Alice")
    joueur2 = Joueur("Bob")
    joueur3 = Joueur("Charlie")
    
    # Créer une partie
    partie = Game([joueur1, joueur2, joueur3])
    
    # Créer un paquet et commencer
    paquet = JeuDeCartes()
    partie.commencer_partie(paquet)
    
    # Vérifier que chaque joueur a 7 cartes
    print(f"{joueur1.nom} a {len(joueur1.cartes)} cartes")
    print(f"{joueur2.nom} a {len(joueur2.cartes)} cartes")
    print(f"{joueur3.nom} a {len(joueur3.cartes)} cartes")
    
    # Tester le tour suivant
    print(f"\nJoueur actuel : {partie.obtenir_joueur_actuel().nom}")
    partie.tour_suivant()
    print(f"Après tour_suivant : {partie.obtenir_joueur_actuel().nom}")
    
    # Tester l'inversion
    partie.inverser_sens()
    partie.tour_suivant()
    print(f"Après inversion et tour : {partie.obtenir_joueur_actuel().nom}")