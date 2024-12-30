from models.weapon import Weapon
from models.enemy import Enemy
from views.game_view import GameView
from views.main_menu_view import MainView

def main():
    axe = Weapon('Curve Axe', 4, 'assets/curve_axe.png', (140, 120))
    helmet_enemy = Enemy('Helmet Enemy', 2, 'assets/enemy.png', (80, 80))
    game_view = GameView(axe, helmet_enemy)
    game = MainView(game_view)
    game.main_loop()
if __name__ == "__main__":
    main()