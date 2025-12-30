# card-check.py / Mathis

import arcade
from arcade import Sprite, SpriteList
import json
from pathlib import Path

script_dir = Path(__file__).parent
with open(script_dir / "card.json") as f:
    cards = json.load(f)

with open(script_dir / "config.json") as f:
    config = json.load(f)

class CardTester(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Card Tester")
        self.sprite_list = SpriteList()
        
        # Extraire tableau des cartes depuis le .json
        self.card_array = cards[0]["card"]
        
        # Liste de toutes les cartes à tester
        self.card_index = 0
        self.all_cards = []
        
        # Collecter tous les IDs de cartes
        for card_item in self.card_array:
            for card_id in card_item.keys():
                self.all_cards.append((card_id, card_item[card_id]))
        
        # Infos de la carte actuelle
        self.current_card_id = ""
        self.current_sprite_name = ""
        self.current_card_info = {}
        
        # Liste des erreurs trouvées
        self.errors = []
        
        # Compteur pour ralentir l'affichage
        self.frame_count = 0
        self.frames_per_card = 10  # Changer carte toutes les 10 frames
        
        # Test terminé
        self.testing_complete = False
        
        # Charger la première carte
        if self.all_cards:
            self.load_card(self.card_index)

    def load_card(self, index):
        # Vider la liste des sprites
        self.sprite_list = SpriteList()
        
        if index >= len(self.all_cards):
            self.testing_complete = True
            return
        
        card_id, card_data = self.all_cards[index]
        self.current_card_id = card_id
        self.current_card_info = card_data
        
        # Extraire les infos de la carte
        card_type = card_data.get("card.type", "N/A")
        card_color = card_data.get("card.color", "N/A")
        card_value = card_data.get("card.value", "N/A")
        sprite_path_str = card_data.get("card.sprite", "N/A")
        
        self.current_sprite_name = sprite_path_str.split("/")[-1] if "/" in sprite_path_str else sprite_path_str
        
        # Vérifier si le sprite existe
        if sprite_path_str != "N/A":
            sprite_path = script_dir.parent / sprite_path_str
            
            if not sprite_path.exists():
                # Enregistrer l'erreur
                error_info = {
                    "card_id": card_id,
                    "sprite_name": self.current_sprite_name,
                    "sprite_path": str(sprite_path),
                    "card_type": card_type,
                    "card_color": card_color,
                    "card_value": card_value,
                    "error": "Fichier sprite manquant"
                }
                self.errors.append(error_info)
                
                # Utiliser BLANK.png
                sprite_path = script_dir.parent / "Assets/Cards/BLANK.png"
            
            try:
                sprite = Sprite(str(sprite_path), center_x=400, center_y=300)
                self.sprite_list.append(sprite)
            except Exception as e:
                # Enregistrer l'erreur de chargement
                error_info = {
                    "card_id": card_id,
                    "sprite_name": self.current_sprite_name,
                    "sprite_path": str(sprite_path),
                    "card_type": card_type,
                    "card_color": card_color,
                    "card_value": card_value,
                    "error": f"Erreur de chargement: {str(e)}"
                }
                self.errors.append(error_info)
        else:
            # Pas de sprite défini
            error_info = {
                "card_id": card_id,
                "sprite_name": "N/A",
                "sprite_path": "N/A",
                "card_type": card_type,
                "card_color": card_color,
                "card_value": card_value,
                "error": "Pas de sprite défini dans le JSON"
            }
            self.errors.append(error_info)

    def on_update(self, delta_time):
        if self.testing_complete:
            return
        
        self.card_index += 1
        
        if self.card_index < len(self.all_cards):
            self.load_card(self.card_index)
        else:
            self.testing_complete = True
            # Vire le dernier sprite
            self.sprite_list = SpriteList()
            self.print_error_report()

    def print_error_report(self):
        print("\n" + "="*60)
        print("RAPPORT DE TEST DES CARTES")
        print("="*60)
        print(f"Total de cartes testées: {len(self.all_cards)}")
        print(f"Erreurs trouvées: {len(self.errors)}")
        print("="*60)
        
        if self.errors:
            for i, error in enumerate(self.errors, 1):
                print(f"\nErreur #{i}:")
                print(f"  ID Carte: {error['card_id']}")
                print(f"  Nom Sprite: {error['sprite_name']}")
                print(f"  Chemin: {error['sprite_path']}")
                print(f"  Type: {error['card_type']}")
                print(f"  Couleur: {error['card_color']}")
                print(f"  Valeur: {error['card_value']}")
                print(f"  Erreur: {error['error']}")
        else:
            print("\nAucune erreur trouvée! Toutes les cartes sont OK.")
        
        print("\n" + "="*60)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        
        if not self.testing_complete:
            # Afficher les infos de la carte en cours de test
            y_pos = self.height - 30
            arcade.draw_text(
                f"Test en cours: {self.card_index + 1}/{len(self.all_cards)}",
                10, y_pos, arcade.color.WHITE, 18, bold=True
            )
            
            y_pos -= 30
            arcade.draw_text(
                f"ID: {self.current_card_id}",
                10, y_pos, arcade.color.WHITE, 16
            )
            
            y_pos -= 25
            arcade.draw_text(
                f"Sprite: {self.current_sprite_name}",
                10, y_pos, arcade.color.WHITE, 16
            )
            
            y_pos -= 25
            card_type = self.current_card_info.get("card.type", "N/A")
            card_color = self.current_card_info.get("card.color", "N/A")
            card_value = self.current_card_info.get("card.value", "N/A")
            arcade.draw_text(
                f"Type: {card_type} | Couleur: {card_color} | Valeur: {card_value}",
                10, y_pos, arcade.color.WHITE, 14
            )
            
            y_pos -= 30
            arcade.draw_text(
                f"Erreurs trouvées: {len(self.errors)}",
                10, y_pos, arcade.color.RED if self.errors else arcade.color.GREEN, 16, bold=True
            )
        else:
            # Test terminé
            arcade.draw_text(
                "TEST TERMINÉ!",
                self.width // 2, self.height // 2 + 50,
                arcade.color.GREEN, 30, bold=True, anchor_x="center"
            )
            
            arcade.draw_text(
                f"Cartes testées: {len(self.all_cards)}",
                self.width // 2, self.height // 2,
                arcade.color.WHITE, 20, anchor_x="center"
            )
            
            arcade.draw_text(
                f"Erreurs: {len(self.errors)}",
                self.width // 2, self.height // 2 - 40,
                arcade.color.RED if self.errors else arcade.color.GREEN, 20, anchor_x="center"
            )
            
            arcade.draw_text(
                "Voir la console pour les détails",
                self.width // 2, self.height // 2 - 80,
                arcade.color.YELLOW, 16, anchor_x="center"
            )


if __name__ == "__main__":
    window = CardTester()
    arcade.run()