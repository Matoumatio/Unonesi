# Coder toutes les classes\methodes liées au multijoueurs
import Gestion_Cartes as Gestion_Cartes
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
        
class Bot:
    pass


class Game:
    def __init__(self, liste_joueurs):
        self.liste_joueurs = liste_joueurs
        self.moteur = MoteurJeu()
        self.paquet = None
        self.defausse = []


    def commencer_partie(self, paquet):

        self.paquet = paquet

        for joueurs in self.liste_joueurs:
            carte_piochees = paquet.piocher(7)
            for carte in carte_piochees:
                joueurs.piocher_carte(carte)

        premiere_carte = paquet.piocher(1)[0]
        self.defausse.append(premiere_carte)

    def obtenir_joueur_actuel(self):
        return self.liste_joueurs[self.moteur.joueur_actuel_index]


    def tour_suivant(self):
        self.moteur.joueur_suivant(len(self.liste_joueurs))

    def inverser_sens(self):
        self.moteur.sens_horaire = not self.moteur.sens_horaire

    def sauter_joueur(self):
        self.tour_suivant()
        self.tour_suivant()

    def obtenir_joueur_actuel(self):
        return self.liste_joueurs[self.joueur_actuel]

    def jouer_tour(self, index_carte):
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
    
    def appliquer_effets(self, effets):
        
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



    

