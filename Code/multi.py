# Coder toutes les classes\methodes liées au multijoueurs

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
        pass

    def tour_suivant(self):
        pass


