from models.weapon import Weapon
from models.enemy import Enemy
from views.game_view import GameView
from views.main_menu_view import MainView
import os


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    axe_path = os.path.join(script_dir, 'assets/curve_axe.png')
    helmet_enemy_path = os.path.join(script_dir, 'assets/enemy.png')
    axe = Weapon('Curve Axe', 4, axe_path, (140, 120))
    helmet_enemy = Enemy('Helmet Enemy', 2, helmet_enemy_path, (80, 80))
    game_view = GameView(axe, helmet_enemy)
    game = MainView(game_view)
    game.main_loop()
if __name__ == "__main__":
    main()