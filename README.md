
# UNONESI
> Dans un but d'apprentissage de la POO (Programation Orientée Objet), la classe d'NSI de Terminale à eu la tâche de créer un projet python l'utilisant

---

### Idées

- Jeu de Cartes
    - Avantages
        - Apprentissage du game design
        - Travail sur les règles
        - Fun et interactif
    - Inconvéniens
        - Complexité des règles
        - Interface joueur
        - Gestion des états du jeu

---

### Ressources

- https://api.arcade.academy/
    - Alternative à Pygame

---

### Fonctionnalités principales

- Initialisation du jeu
    - Créer un paquet de 108 cartes
    - Les mélanger et distribuer 7 cartes par joueur
- Gestion des tours
    - Alterner les tours entre les joueurs
    - Gérer le sens du jeu
- Joueur une carte
    - Permettre à un joueur de poser une carte compatible avec la défausse
- Piocher une carte
    - Si un joueur ne peut pas jouer, il pioche une carte
- Appliquer les effets des cartes spéciales
    - +2, +4, Inversion, Passe, Joker, ...
- Détection de la fin de partie
    - Détecter quand un joueur n'a plus de cartes et annoncer le gagnant
- Interface graphique
    - Afficher les cartes des joueurs, la défausse, et les informations du jeu
    - Permettre aux joueurs de sélectionner et jouer des cartes via l'interface

---

### Fonctionnalités avancées (optionnelles)

- Sauvegarder l'état du jeu en JSON et le recharger
- Afficher l'état du jeu et les actions possibles
- Un joueur automatisé capabe de joueur selon des règles simples
- Afficher le nombre de tours, de cartes jouées, etc...

---

### Répartition des rôles

- Interface : Mathis
- Mécaniques de jeu : Tom
- Multijoueur :  Nathan
- Gestion des cartes : Shirley

---

### Journal de bord

- 16/10/2025 : Brainstorming idées, initialisation de github pour toute l'équipe
- 06/11/2025 : Répartitions des rôles et idées principales du projet, préparation des sprites, mise en commun des règles du jeu
- 12/11/2025 : Avancement individuel dans le projet suite aux répartitions des différentes tâches, Mathis sur l'interface, Nathan sur le système de multijoueur, Shirley sur la gestion des différentes cartes dans le jeu et Tom sur le fonctionnement du jeu et l'implémentation des règles du jeu 
    - Mathis : Recherche sur la bibliothèque Pygame, brouillon de l'interface et recherche des assets
![Brouillon de l'interface de jeu](https://raw.githubusercontent.com/Matoumatio/Unonesi/refs/heads/main/Assets/RM/Brouillon1.png)
    - Tom : Recherche sur les différentes classes à implémenter pour les mécaniques du jeu : class Carte et MoteurJeu 
- 19/11/2025
    - Mathis : Recherches sur Aseprite (https://www.aseprite.org/) et Arcade (https://api.arcade.academy/) pour la création des sprites et l'interface graphique, création de brouillons plus détaillés de l'interface de jeu et du menu de pause
![Brouillon détaillé de l'interface de jeu](https://raw.githubusercontent.com/Matoumatio/Unonesi/refs/heads/main/Assets/RM/Brouillon2.png)
![Brouillon détaillé du menu de pause](https://raw.githubusercontent.com/Matoumatio/Unonesi/refs/heads/main/Assets/RM/Brouillon3.png)
![Brouillon détaillé du menu de paramètres](https://raw.githubusercontent.com/Matoumatio/Unonesi/refs/heads/main/Assets/RM/Brouillon4.png)
    - Tom : Avancement sur les mêmes classes 
- 27/11/2025
    - Tom : Correction de bug sur les classes et sur l'ensemble du code et essaie du code déjà en place avec des asserts
    - Nathan : Essaie d'import les classes cartes dans le fichier multi. Avancement des methodes de la class Game
    - Mathis : Ajout de constants.json pour syncroniser les valeurs (sauvegardes, paramètres, ...) entre les fichiers
    ![Brouillon non détaillé des différentes parties de programmation pour la sélection des cartes et l'IA](https://raw.githubusercontent.com/Matoumatio/Unonesi/refs/heads/main/Assets/RM/Brouillon5.png)
    - Shirley : Travail sur card.json pour definir les différentes cartes disponibles
- 04/12/2025
    - Tom : Finalisation du code avec la mise en place de:
        - *RÈGLE PRINCIPALE : Est-ce que je peux poser cette carte ?
        - *ACTIONS DE JEU : Que se passe-t-il quand on joue une carte ?
        - *GESTION DES TOURS : Qui joue après ?
        - *RÈGLE DE LA PIOCHE : Quand et comment piocher ?
        - *DÉBUT DE PARTIE : Que se passe-t-il selon la première carte ?
        - *RÈGLE UNO : Annonce obligatoire
        - *FIN DE PARTIE : Détecter le gagnant et compter les points
        - (*DÉFI DU +4 (BONUS - règle avancée))
    - Mathis : Travail sur le sprite des cartes
    ![Sprite des cartes](https://raw.githubusercontent.com/Matoumatio/Unonesi/refs/heads/main/Assets/RM/Brouillon6.png)
- 08/12/2025
    - Mathis
        - Ajout des cartes chiffres + carte placeholder
        - Ajout de card-test.py et card-random.py pour tester Arcade et vérifier que les fichiers marchent ensembles
            - card-test.py --> Teste l'ensemble des cartes et affiche si des problèmes sont survenus
            - card-random.py --> Affiche une carte aléatoire, appuyez sur "R" pour une nouvelle carte
        - Modification des ID dans card.json car problèmes
        - [A FAIRE] : Modifier les incohérences entre les sprites (pixel en trop, nombres mal placés, ...)
    - Tom
       -avancement du projet(fin) + correction de bug 

- 11/12/2025
    - Tom
       -Finalité de la partie du code avec les derniers attributs et ajout de commentaire compréhensible et permettant de se repérer dans le code
---
 