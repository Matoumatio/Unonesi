#coder les mecaniques de jeu et les regles en poo

#Travail sur le fonctionnement du jeu (resume : en gros)

#si dans le paquet (utiliser fifo) Exemple : si dans le paquet ya 7 jaune 
#la personne est oblige de jouer une carte jaune ou un 7
#voir reste des regle puis faire pareil

#Regles:
#voir regle site (toutes sauf les trois dernieres) regles classique 
# (regle : si on pioche une bonne carte, on peut rejouer direct, si on se prend une sanction
#et qu'on pioche on ne peut pas rejouer) 

class Carte:
    def __init__(self, couleur, valeur, type_carte):
        # CORRECTION : Stocker les paramètres comme attributs
        self.couleur = couleur
        self.valeur = valeur
        self.type_carte = type_carte
        
    def __str__(self):
        # CORRECTION : Implémentation
        if self.couleur is None:
            return f"[{self.valeur}]"
        return f"[{self.couleur} {self.valeur}]"
        
    def est_jouable(self, carte_visible, couleur_actuelle):
        # CORRECTION : Cette méthode devrait être supprimée ou déléguée au MoteurJeu
        # Une carte ne devrait pas connaître les règles du jeu
        pass  # À supprimer, utiliser MoteurJeu.carte_est_compatible à la place



# Importer class carte Shirley

class MoteurJeu:
    def __init__(self):
        self.carte_visible = None
        self.couleur_actuelle = None
        self.sens_horaire = True
        self.joueur_actuel_index = 0
        
    def carte_est_compatible(self, carte, carte_visible, couleur_actuelle):
        # CORRECTION : Implémenter la logique
        if carte_visible is None:
            return True
        
        if carte.type_carte == "joker":
            return True
        
        if carte.couleur == couleur_actuelle:
            return True
        
        if carte.valeur == carte_visible.valeur:
            return True
        
        return False
        
    def carte_plus4_est_legale(self, main_joueur, couleur_actuelle):
        # CORRECTION : Ajouter le paramètre 'carte' et implémenter
        if Carte.valeur != "+4":
            return True
        
        for c in main_joueur:
            if c.couleur == couleur_actuelle:
                return False
        
        return True
    