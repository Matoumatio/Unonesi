# card-random.py / Mathis

import arcade
from arcade import Sprite, SpriteList
import json
import random
from pathlib import Path

script_dir = Path(__file__).parent
with open(script_dir / "card.json") as f:
    cards = json.load(f)

with open(script_dir / "config.json") as f:
    config = json.load(f)

class CardWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Card Viewer")
        self.sprite_list = SpriteList()
        
        # Extraire tableau des cartes depuis le .json
        self.card_array = cards[0]["card"]
        
        # Stocker l'ID de la carte actuelle et le nom du sprite
        self.current_card_id = ""
        self.current_sprite_name = ""
        
        # Charger une première carte
        self.load_random_card()

    def load_random_card(self):
        # Vider la liste des sprites
        self.sprite_list = SpriteList()
        
        random_card_num = random.randint(1, 40)
        random_card_id = f"card_{random_card_num:03d}"
        
        # Sauvegarder l'ID de la carte
        self.current_card_id = random_card_id
        
        card_data = None
        
        # Cherche la carte
        for card_item in self.card_array:
            if random_card_id in card_item:
                card_data = card_item[random_card_id]
                break
        
        # Créer le sprite depuis le chemin de l'image
        if card_data and "card.sprite" in card_data:
            sprite_path = script_dir.parent / card_data["card.sprite"]
            # Sauvegarder le nom du fichier sprite
            self.current_sprite_name = card_data["card.sprite"].split("/")[-1]
            
            # Vérifier si le fichier existe, sinon utiliser BLANK.png
            if not sprite_path.exists():
                sprite_path = script_dir.parent / "Assets/Cards/BLANK.png"
                self.current_sprite_name = "BLANK.png (sprite manquant)"
            
            sprite = Sprite(str(sprite_path), center_x=400, center_y=300)
            self.sprite_list.append(sprite)
        else:
            # Si la carte n'est pas trouvée dans le JSON, utiliser BLANK.png
            sprite_path = script_dir.parent / "Assets/Cards/BLANK.png"
            self.current_sprite_name = "BLANK.png (carte non trouvée)"
            sprite = Sprite(str(sprite_path), center_x=400, center_y=300)
            self.sprite_list.append(sprite)

    def on_key_press(self, key, modifiers):
        # Quand on appuie sur "r", charger une nouvelle carte
        if key == arcade.key.R:
            self.load_random_card()

    def on_draw(self):
        self.clear()
        self.sprite_list.draw()
        
        # Afficher l'ID de la carte et le nom du sprite dans le coin supérieur gauche
        arcade.draw_text(
            f"{self.current_card_id} - {self.current_sprite_name}",
            10, 
            self.height - 30,
            arcade.color.WHITE,
            20,
            bold=True
        )


if __name__ == "__main__":
    window = CardWindow()
    arcade.run()