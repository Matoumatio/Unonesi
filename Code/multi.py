# multi.py / Nathan

# Coder toutes les classes\methodes liées au multijoueurs
import random
from Gestion_Cartes import Carte, JeuDeCartes
from regle_meca import MoteurJeu


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
        self.moteur = MoteurJeu()
        self.paquet = None
        self.defausse = []


    def commencer_partie(self, paquet):

        self.paquet = paquet

        # Distribue 7 cartes à chaque joueur
        for joueurs in self.liste_joueurs:
            carte_piochees = paquet.piocher(7)
            for carte in carte_piochees:
                joueurs.piocher_carte(carte)

        # Retourne la première carte de la fausse
        premiere_carte = paquet.piocher(1)[0]
        self.defausse.append(premiere_carte)

        self.moteur.carte_visible = premiere_carte
        self.moteur.couleur_actuelle = premiere_carte.couleur

    def obtenir_joueur_actuel(self):
        return self.liste_joueurs[self.moteur.joueur_actuel_index]


    def tour_suivant(self):
        self.moteur.joueur_suivant(len(self.liste_joueurs))

    def inverser_sens(self):
        self.moteur.sens_horaire = not self.moteur.sens_horaire

    def sauter_joueur(self):
        self.tour_suivant()
        self.tour_suivant()


    def jouer_tour(self, index_carte, couleur_choisie=None):
        """ Gere un tour entier """
        
        # Récupere le joueur actuel et la carte à jouer
        joueur = self.obtenir_joueur_actuel()
        carte_a_jouer = joueur.cartes[index_carte]

        # Récupere la carte visible
        carte_visible = self.defausse[-1] if self.defausse else None

        # Vérifie si la carte est jouable
        if not self.moteur.carte_est_jouable(carte_a_jouer):
            return False, "Cette carte n'est pas jouable"
        
        # Joue la carte
        carte_jouee = joueur.jouer_carte(index_carte)
        self.defausse.append(carte_jouee)

        # Met a jour
        succes, message = self.moteur.jouer_carte(carte_jouee, joueur.cartes)

        if not succes:
            return False, message
        
        # Applique les effets de la carte
        effets = self.moteur.appliquer_effet_carte(carte_jouee, len(self.liste_joueurs))

        # Gere les effets
        self._appliquer_effets(effets)

        # Passe au joueur suivant
        if not effets['sauter_tour']:
            self.tour_suivant()
        else:
            self.sauter_joueur()

        return True, "Carte jouée"
    
    def _appliquer_effets(self, effets):
        
        # Si quelqu'un doit piocher
        if effets['piocher'] > 0:
            if effets['qui_pioche'] == "joueur_suivant":
                # Calculer qui est le joueur suivant
                index_suivant = self.moteur.joueur_suivant(len(self.liste_joueurs))
                joueur_suivant = self.liste_joueurs[index_suivant]
                
                # Faire piocher
                for _ in range(effets['piocher']):
                  if len(self.paquet.cartes) > 0:
                    carte = self.paquet.piocher(1)[0]
                    joueur_suivant.piocher_carte(carte)

    def obtenir_cartes_jouables(self, joueur):
        """ Retourne une liste des index des cartes jouables pour un joueur"""
        cartes_jouables = []

        for i, carte in enumerate(joueur.cartes):
            if self.moteur.carte_est_jouable(carte):
                cartes_jouables.append(i)

        return cartes_jouables
    
    def piocher_carte_obligatoire(self):
        """ Le joueur doit piocher car il ne peut pas jouer"""
        joueur = self.obtenir_joueur_actuel()


        if len(self.paquet.cartes) > 0:
            carte = self.paquet.piocher(1)[0]
            joueur.piocher_carte(carte)

            # Verifie si la carte joué est jouable
            if self.moteur.peut_rejouer_carte_piochee(carte, est_sanction=False):
                return True, carte  # Le joueur joue la carte
            else:
                self.tour_suivant()
                return False, carte # Le joueur passe son tour
            
        return False, None  # Paquet Vide
    
    def verifier_fin_partie(self):
        """Vérifie si un joueur a gagné"""
        for joueur in self.liste_joueurs:
            if len(joueur.cartes) == 0:
                return True, joueur
        
        return False, None
    
    def choisir_couleur_joker(self, couleur):
        """Le joueur choisit une couleur après avoir joué un joker"""
        if couleur in ["rouge", "jaune", "bleu", "vert"]:
            self.moteur.couleur_actuelle = couleur
            return True
        return False
    
    def calculer_scores(self, gagnant):
        """Calcule le score du gagnant"""
        score_total = 0
        for joueur in self.liste_joueurs:
            if joueur != gagnant:
                score_total += self.moteur.calculer_points(joueur.cartes)
        return score_total
    
    def choisir_couleur_automatique(self, joueur):
        """Choisit automatiquement la couleur la plus présente dans la main du bot joueur"""
        # Compter les couleurs dans la main
        compteur_couleurs = {'rouge': 0, 'jaune': 0, 'vert': 0, 'bleu': 0}
        
        for carte in joueur.cartes:
            if carte.couleur in compteur_couleurs:
                compteur_couleurs[carte.couleur] += 1
        
        # Trouver la couleur la plus fréquente
        couleur_max = max(compteur_couleurs, key=compteur_couleurs.get)
        
        return couleur_max
