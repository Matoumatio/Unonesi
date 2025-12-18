# ui.py / Mathis

import arcade
from arcade import Sprite, SpriteList
import json
from pathlib import Path


script_dir = Path(__file__).parent
with open(script_dir / "card.json") as f:
    cards = json.load(f)

with open(script_dir / "config.json") as f:
    config = json.load(f)

class Unonesi(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Unonesi")
        self.sprite_list = SpriteList()

if __name__ == "__main__":
    window = Unonesi()
    arcade.run()
