import random
import json

import constants.json as constants
import card.json as card

class Pioche:
    "Donne une carte à l'aide d'un random en fonction de l'ID des cartes de card.json"
    
    def piocher(self):
        carte_choisie = random.choice(list(card.keys()))
        return carte_choisie
    def piocher_multiple(self, nombre):
        cartes_choisies = random.choices(list(card.keys()), k=nombre)
        return cartes_choisies

if __name__ == "__main__":
    pioche = Pioche()
    print(pioche.piocher())
    print(pioche.piocher_multiple(5))
    