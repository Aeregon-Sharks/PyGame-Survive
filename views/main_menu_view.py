import pygame
import sys

class MainView:
    def __init__(self, game_controller):
        pygame.init()
        # Screen properties
        self.WIDTH, self.HEIGHT = 1280, 720
        self.BG_COLOR = (8, 0, 13)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        # Game controller
        self.game_controller = game_controller
        self.game_controller.set_screen(self.screen)
        # Text properties
        self.FONT = pygame.font.SysFont('animematrixmben', 36)
        self.TEXT_COLOR = (255, 255, 255)
        # Game states
        self.MENU = "menu"
        self.PLAYING = "playing"
        self.PAUSE = "pause"
        self.GAME_OVER = "game_over"
        self.INSTRUCTIONS = "instructions"
        self.current = self.MENU
        # Button areas
        self.menu_buttons = {}
        self.pause_buttons = {}
        # others
        self.high_score = 0
        self.difficulties = {'Facil':{'enemy_speed':2, 'player_speed':4, 'spawn_chance':0.02, 'given_points': 1},
                             'Normal':{'enemy_speed':4, 'player_speed':6, 'spawn_chance':0.04, 'given_points': 2},
                             'Dificil':{'enemy_speed':6, 'player_speed':8, 'spawn_chance':0.06, 'given_points': 3},
                             'Imposible':{'enemy_speed':10, 'player_speed':10, 'spawn_chance':0.08, 'given_points': 5}}
        self.selected_diff = 'Facil'

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x, y))
        surface.blit(text_obj, text_rect)
        return text_rect

    def main_menu(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_text("Menu Principal", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 4)
        if self.game_controller.points > self.high_score:
            self.high_score = self.game_controller.points
        self.draw_text("Puntaje mas alto: " + str(self.high_score), self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 4 + 40)
        # Draw and store button rects
        self.menu_buttons["start"] = self.draw_text("1. Iniciar Juego", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 - 20)
        self.menu_buttons["quit"] = self.draw_text("2. Salir", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 20)
        self.menu_buttons["difficulty"] = self.draw_text("3. Dificultad: " + self.selected_diff, self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 60)
        self.menu_buttons["instructions"] = self.draw_text("4. Instrucciones", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 100)
        pygame.display.flip()

    def pause_menu(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_text("Pausa", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 4)
        # Draw and store button rects
        self.pause_buttons["resume"] = self.draw_text("1. Continuar", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 - 20)
        self.pause_buttons["menu"] = self.draw_text("2. Salir al Menu Principal", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 20)
        pygame.display.flip()
    
    def game_over_menu(self):
        self.screen.fill(self.BG_COLOR)
        if self.game_controller.points > self.high_score:
            self.high_score = self.game_controller.points
        self.draw_text("Game Over", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 4)
        self.draw_text('Presiona R para reiniciar', self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 - 20)
        self.draw_text("Presiona Enter para regresar al Menu Principal", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 20)
        pygame.display.flip()
    
    def instructions_menu(self):
        self.screen.fill(self.BG_COLOR)
        self.draw_text("Instrucciones", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 4)
        self.draw_text("Muevete con W, A, S, D", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 - 20)
        self.menu_buttons['Volver'] = self.draw_text("1. Volver", self.FONT, self.TEXT_COLOR, self.screen, self.WIDTH // 2, self.HEIGHT // 2 + 20)
        pygame.display.flip()

    def playing(self):
        if self.game_controller.started == False:
            self.game_controller.start_game(self.difficulties[self.selected_diff])
        else:
            self.game_controller.game_loop()

    def main_loop(self):
        clock = pygame.time.Clock()
        while True:
            # Event handling
            # Pause event flag
            if self.game_controller.paused == True:
                self.current = self.PAUSE
            if self.game_controller.alive == False:
                self.current = self.GAME_OVER
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Mouse click event
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    mouse_pos = event.pos
                    if self.current == self.MENU:
                        if self.menu_buttons["start"].collidepoint(mouse_pos):
                            self.current = self.PLAYING
                        elif self.menu_buttons["quit"].collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
                        elif self.menu_buttons["difficulty"].collidepoint(mouse_pos):
                            self.cycle_diff()
                        elif self.menu_buttons["instructions"].collidepoint(mouse_pos):
                            self.current = self.INSTRUCTIONS
                    elif self.current == self.PAUSE:
                        if self.pause_buttons["resume"].collidepoint(mouse_pos):
                            self.current = self.PLAYING
                        elif self.pause_buttons["menu"].collidepoint(mouse_pos):
                            self.current = self.MENU
                            self.game_controller.paused = False
                            self.game_controller.started = False
                    elif self.current == self.INSTRUCTIONS:
                        if self.menu_buttons['Volver'].collidepoint(mouse_pos):
                            self.current = self.MENU
                # Key press event
                if event.type == pygame.KEYDOWN:
                    if self.current == self.MENU:
                        if event.key == pygame.K_1:
                            self.current = self.PLAYING
                            self.game_controller.started = False
                        elif event.key == pygame.K_2:
                            pygame.quit()
                            sys.exit()
                        elif event.key == pygame.K_3:
                            self.cycle_diff()
                        elif event.key == pygame.K_4:
                            self.current = self.INSTRUCTIONS
                    # Playing
                    elif self.current == self.PLAYING:
                        if event.key == pygame.K_ESCAPE:
                            self.current = self.PAUSE
                    # Pause Menu
                    elif self.current == self.PAUSE:
                        if event.key == pygame.K_1:
                            self.current = self.PLAYING
                        elif event.key == pygame.K_2:
                            self.current = self.MENU
                            self.game_controller.paused = False
                            self.game_controller.started = False
                    # Instructions
                    elif self.current == self.INSTRUCTIONS:
                        if event.key == pygame.K_1:
                            self.current = self.MENU
                    # Game Over
                    elif self.current == self.GAME_OVER:
                        if event.key == pygame.K_RETURN:
                            self.current = self.MENU
                            self.game_controller.started = False
                            self.game_controller.alive = True
                        if event.key == pygame.K_r:
                            self.current = self.PLAYING
                            self.game_controller.started = False
                            self.game_controller.alive = True
            # Game states
            if self.current == self.MENU:
                self.main_menu()
            elif self.current == self.PLAYING:
                self.playing()
            elif self.current == self.PAUSE:
                self.pause_menu()
            elif self.current == self.GAME_OVER:
                self.game_over_menu()
            elif self.current == self.INSTRUCTIONS:
                self.instructions_menu()
            clock.tick(60)

    def cycle_diff(self):
        if self.selected_diff == 'Facil':
            self.selected_diff = 'Normal'
        elif self.selected_diff == 'Normal':
            self.selected_diff = 'Dificil'
        elif self.selected_diff == 'Dificil':
            self.selected_diff = 'Imposible'
        else:
            self.selected_diff = 'Facil'