import random

def Carte():
    class cartes:
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

# Exemple d'utilisation :
jeu = JeuDeCartes()
print(len(jeu.cartes))  
print(jeu.piocher(7)) 