#coder les mecaniques de jeu et les regles en poo

#Travail sur le fonctionnement du jeu (resume : en gros)

#si dans le paquet (utiliser fifo) Exemple : si dans le paquet ya 7 jaune 
#la personne est oblige de jouer une carte jaune ou un 7
#voir reste des regle puis faire pareil

#Regles:
#voir regle site (toutes sauf les trois dernieres) regles classique 
# (regle : si on pioche une bonne carte, on peut rejouer direct, si on se prend une sanction
#et qu'on pioche on ne peut pas rejouer) 
#
class MoteurJeu:
    """
    Classe qui gère TOUTES les mécaniques et règles du UNO
    Vérifie si les actions sont autorisées selon les règles officielles
    """
    
    def __init__(self):
        self.carte_visible = None           # Dernière carte jouée (ex: 7 jaune)
        self.couleur_actuelle = None        # Couleur en cours (rouge, jaune, vert, bleu)
        self.sens_horaire = True            # Sens du jeu
        self.joueur_actuel_index = 0        # Index du joueur dont c'est le tour
    
    # ========================================================================
    # RÈGLE PRINCIPALE : Est-ce que je peux poser cette carte ?
    # ========================================================================
    
    def carte_est_jouable(self, carte_a_jouer):
        """
        RÈGLE FONDAMENTALE DU UNO :
        Une carte peut être posée SI :
        - Même couleur que la couleur actuelle (7 jaune sur n'importe quel jaune)
        - OU même valeur que la carte visible (7 jaune sur 7 rouge)
        - OU c'est un Joker ou +4
        
        Exemples :
        - 7 jaune sur 7 rouge : OUI (même valeur)
        - carte jaune sur 7 jaune : OUI (même couleur)
        - 5 rouge sur 7 jaune : NON
        - Joker sur n'importe quoi : OUI
        """
        # Les jokers peuvent TOUJOURS être joués peut importe la carte d'avant
        if carte_a_jouer.valeur in ['joker', '+4']:
            return True
        
        # Même couleur (ex: n'importe quel jaune sur un 2 jaune)
        if carte_a_jouer.couleur == self.couleur_actuelle:
            return True
        
        # Même valeur (ex: 8 jaune sur 8 rouge)
        if carte_a_jouer.valeur == self.carte_visible.valeur:
            return True
        
        # Sinon : interdit
        return False
    
    def carte_plus4_est_legale(self, main_joueur):
        """
        RÈGLE SPÉCIALE DU +4 :
        Le +4 ne peut être joué QUE si le joueur n'a AUCUNE carte
        de la couleur demandée
        
        Exemple : Si couleur actuelle = jaune
        - Le joueur a un 5 rouge et un +4 : +4 est LÉGAL
        - Le joueur a un 5 jaune et un +4 : +4 est ILLÉGAL (il doit jouer le jaune)
        """
        for carte in main_joueur:
            if carte.couleur == self.couleur_actuelle:
                return False  # Il a une carte de la bonne couleur = triche !
        return True  # Aucune carte de la couleur = OK
    
    # ========================================================================
    # ACTIONS DE JEU : Que se passe-t-il quand on joue une carte ?
    # ========================================================================
    
    def jouer_carte(self, carte_jouee, main_joueur, couleur_choisie=None):
        """
        Joue une carte si c'est autorisé
        
        Étapes :
        1. Vérifie si la carte est jouable
        2. Met à jour la carte visible et la couleur actuelle
        3. Retourne True si succès, False si interdit
        """
        # Vérifier si la carte est autorisée a etre posé
        if not self.carte_est_jouable(carte_jouee):
            return False, "Carte non compatible !"
       
        # Mettre à jour la carte visible
        self.carte_visible = carte_jouee
        
        # Mettre à jour la couleur actuelle
        if carte_jouee.couleur != 'noir':
            # Carte normale : la couleur devient celle de la carte
            self.couleur_actuelle = carte_jouee.couleur
        elif couleur_choisie:
            # Joker ou +4 : le joueur choisit la couleur
            self.couleur_actuelle = couleur_choisie
        
        return True, "Carte jouée !"
    
    def appliquer_effet_carte(self, carte_jouee, nombre_joueurs):
        """
        Applique les effets des cartes spéciales
        
        Retourne un dictionnaire avec les actions à effectuer :
        {
            'piocher': nombre de cartes à piocher (0 si rien),
            'qui_pioche': 'joueur_suivant' ou None,
            'sauter_tour': True/False,
            'peut_rejouer_apres_pioche': True/False
        }
        """
        effet = {
            'piocher': 0,
            'qui_pioche': None,
            'sauter_tour': False,
            'peut_rejouer_apres_pioche': False
        }
        
        # CARTE +2 : Le joueur suivant pioche 2 et PASSE son tour
        if carte_jouee.valeur == '+2':
            effet['piocher'] = 2
            effet['qui_pioche'] = 'joueur_suivant'
            effet['sauter_tour'] = True
            effet['peut_rejouer_apres_pioche'] = False  # Sanction = pas de rejeu
        
        # CARTE INVERSE : Change le sens du jeu
        elif carte_jouee.valeur == 'inverse':
            self.sens_horaire = not self.sens_horaire
            # Si 2 joueurs : équivaut à "passe ton tour"
            if nombre_joueurs == 2:
                effet['sauter_tour'] = True
        
        # CARTE PASSE : Le joueur suivant est sauté
        elif carte_jouee.valeur == 'passe':
            effet['sauter_tour'] = True
        
        # CARTE +4 : Le joueur suivant pioche 4 et PASSE son tour
        elif carte_jouee.valeur == '+4':
            effet['piocher'] = 4
            effet['qui_pioche'] = 'joueur_suivant'
            effet['sauter_tour'] = True
            effet['peut_rejouer_apres_pioche'] = False  # Sanction = pas de rejeu
        
        # CARTE JOKER : Pas d'effet spécial (juste changement de couleur)
        # CARTES NUMÉRIQUES : Pas d'effet
        
        return effet
    
    # ========================================================================
    # GESTION DES TOURS : Qui joue après ?
    # ========================================================================
    
    def joueur_suivant(self, nombre_joueurs):
        """
        Calcule qui est le joueur suivant selon le sens du jeu
        
        Sens horaire ou Sens anti-horaire 
        """
        if self.sens_horaire:
            self.joueur_actuel_index = (self.joueur_actuel_index + 1) % nombre_joueurs
        else:
            self.joueur_actuel_index = (self.joueur_actuel_index - 1) % nombre_joueurs
        
        return self.joueur_actuel_index
    
    def sauter_joueur(self, nombre_joueurs):
        """
        Saute le joueur suivant (pour les cartes Passe, +2, +4)
        """
        # On avance deux fois
        self.joueur_suivant(nombre_joueurs)
        self.joueur_suivant(nombre_joueurs)
        return self.joueur_actuel_index
    
    # ========================================================================
    #  RÈGLE DE LA PIOCHE : Quand et comment piocher ?
    # ========================================================================
    
    def peut_rejouer_carte_piochee(self, carte_piochee, est_sanction):
        """
        RÈGLE IMPORTANTE :
        
        - Si pioche VOLONTAIRE (le joueur ne peut pas jouer) :
          → Si la carte piochée est jouable : il PEUT la jouer immédiatement
          → Sinon : il passe son tour
        
        - Si pioche de SANCTION (+2, +4) :
          → Le joueur pioche et PASSE son tour (pas le droit de rejouer après avoir piocher)
        """
        # Si c'est une sanction : JAMAIS de rejeu
        if est_sanction:
            return False
        
        # Si pioche volontaire : on peut rejouer si la carte est compatible
        return self.carte_est_jouable(carte_piochee)
    
    # ========================================================================
    # DÉBUT DE PARTIE : Que se passe-t-il selon la première carte ?
    # ========================================================================
    
    def gerer_premiere_carte(self, premiere_carte, nombre_joueurs, donneur_index):
        """
        RÈGLES SPÉCIALES SELON LA PREMIÈRE CARTE RETOURNÉE :
        
        - +2 : Premier joueur pioche 2 et passe son tour
        - Inverse : Le donneur joue en premier, puis sens inversé
        - Passe : Premier joueur est sauté
        - Joker : Premier joueur choisit la couleur
        - +4 : ON REMET DANS LA PIOCHE et on retourne une autre carte
        - Autre : Partie normale
        
        Retourne : (premier_joueur_index, action_speciale)
        """
        self.carte_visible = premiere_carte
        
        # CAS +4 : Carte interdite au début
        if premiere_carte.valeur == '+4':
            return None, 'remettre_dans_pioche'
        
        # CAS +2
        elif premiere_carte.valeur == '+2':
            self.couleur_actuelle = premiere_carte.couleur
            premier_joueur = (donneur_index + 1) % nombre_joueurs
            return premier_joueur, {'piocher': 2, 'sauter': True}
        
        # CAS INVERSE
        elif premiere_carte.valeur == 'inverse':
            self.couleur_actuelle = premiere_carte.couleur
            self.sens_horaire = not self.sens_horaire
            # Le donneur joue en premier
            return donneur_index, None
        
        # CAS PASSE
        elif premiere_carte.valeur == 'passe':
            self.couleur_actuelle = premiere_carte.couleur
            # On saute le premier joueur
            premier_joueur = (donneur_index + 1) % nombre_joueurs
            prochain = (premier_joueur + 1) % nombre_joueurs
            return prochain, None
        
        # CAS JOKER
        elif premiere_carte.valeur == 'joker':
            premier_joueur = (donneur_index + 1) % nombre_joueurs
            return premier_joueur, 'choisir_couleur'
        
        # CAS NORMAL (carte numérique)
        else:
            self.couleur_actuelle = premiere_carte.couleur
            premier_joueur = (donneur_index + 1) % nombre_joueurs
            return premier_joueur, None
    
    # ========================================================================
    # RÈGLE UNO : Annonce obligatoire
    # ========================================================================
    
    def verifier_uno(self, joueur_cartes_restantes, a_dit_uno):
        """
        RÈGLE UNO :
        - Quand un joueur pose son avant-dernière carte (il lui reste 1 carte),
          il DOIT dire "UNO"
        - Si il oublie et qu'un autre joueur le remarque :
          → Il pioche 2 cartes de pénalité
        
        Retourne : nombre de cartes à piocher en pénalité (0 ou 2)
        """
        if joueur_cartes_restantes == 1 and not a_dit_uno:
            return 2  # Pénalité : 2 cartes
        return 0  # Pas de pénalité
    
    # ========================================================================
    # FIN DE PARTIE : Détecter le gagnant et compter les points
    # ========================================================================
    
    def partie_terminee(self, joueur_cartes_restantes):
        """
        La partie se termine quand un joueur n'a plus de cartes
        """
        return joueur_cartes_restantes == 0
    
    def calculer_points(self, main_adversaire):
        """
        RÈGLE COMPTAGE DES POINTS :
        - Cartes 0-9 : valeur du chiffre
        - +2, Inverse, Passe : 20 points
        - Joker, +4 : 50 points
        
        Le gagnant marque la somme des points des cartes
        des autres joueurs
        """
        points = 0
        for carte in main_adversaire:
            if isinstance(carte.valeur, int):
                points += carte.valeur  # 0-9
            elif carte.valeur in ['+2', 'inverse', 'passe']:
                points += 20
            elif carte.valeur in ['joker', '+4']:
                points += 50
        return points



# TESTS / EXEMPLES D'UTILISATION
"""
if __name__ == "__main__":
    # Simulation pour tester les mécaniques
    from shirley_code import Carte  # Import du code de Shirley
    
    moteur = MoteurJeu()
    
    # Test 1 : 7 jaune sur 7 rouge
    moteur.carte_visible = Carte('rouge', 7)
    moteur.couleur_actuelle = 'rouge'
    
    carte_test = Carte('jaune', 7)
    print("Test : 7 jaune sur 7 rouge")
    print(f"Jouable ? {moteur.carte_est_jouable(carte_test)}")  # True
    
    # Test 2 : carte jaune sur 7 jaune
    moteur.carte_visible = Carte('jaune', 7)
    moteur.couleur_actuelle = 'jaune'
    
    carte_test2 = Carte('jaune', 3)
    print("\nTest : 3 jaune sur 7 jaune")
    print(f"Jouable ? {moteur.carte_est_jouable(carte_test2)}")  # True
    
    # Test 3 : 5 rouge sur 7 jaune (INTERDIT)
    carte_test3 = Carte('rouge', 5)
    print("\nTest : 5 rouge sur 7 jaune")
    print(f"Jouable ? {moteur.carte_est_jouable(carte_test3)}")  # False
    
    # Test 4 : Joker sur n'importe quoi
    carte_test4 = Carte('noir', 'joker')
    print("\nTest : Joker sur 7 jaune")
    print(f"Jouable ? {moteur.carte_est_jouable(carte_test4)}")  # True
    
    # Test 5 : Effet d'un +2
    carte_plus2 = Carte('rouge', '+2')
    effet = moteur.appliquer_effet_carte(carte_plus2, 4)
    print("\nTest : Effet +2")
    print(f"Effet : {effet}")
    
    print("\n✅ Tests terminés !")
"""