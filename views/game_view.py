import pygame
import sys
import math
import random

class GameView():

    def __init__(self, weapon, enemy):
        # Paused flag
        self.paused = False
        # Objects
        self.weapon = weapon
        self.enemy = enemy
        # Window properties
        self.WIDTH, self.HEIGHT = 1280, 720
        self.screen = None
        self.started = False
        # Player properties
        self.active_right_hb = False
        self.active_left_hb = True
        self.lives = 3
        self.alive = True
        self.points = 0

    def set_screen(self, screen):
        self.screen = screen

    def start_game(self, args):
        self.points = 0
        self.bg_color = (8, 0, 13)
        self.lives = 3
        self.alive = True
        self.started = True
        self.given_points = args['given_points']
        self.enemy_spawn_chance = args['spawn_chance']
        # Player and enemy initial positions
        self.pos_x = self.WIDTH // 2
        self.pos_y = self.HEIGHT // 2
        self.enemies = [(20, 20, self.enemy_hitbox(20, 20))]
        # Asset properties
        self.player_speed = args['player_speed']
        self.enemy_speed = args['enemy_speed']
        # Load assets from objects
        self.weapon_img = pygame.image.load(self.weapon.image_path).convert_alpha()
        self.weapon_img = pygame.transform.scale(self.weapon_img, self.weapon.dims)
        self.inverted_weapon_img = pygame.transform.flip(self.weapon_img, True, False)
        
        self.enemy_img = pygame.image.load(self.enemy.image_path).convert_alpha()
        self.enemy_img = pygame.transform.scale(self.enemy_img, self.enemy.dims)

        self.empty_heart = pygame.image.load("assets/empty_heart.png")
        self.full_heart = pygame.image.load("assets/full_heart.png")
        # Game loop
        self.clock = pygame.time.Clock()
        self.game_loop()

    def game_loop(self):
        self.paused = False
        playing = True
        # Movement flags for strafe
        move_left = False
        move_right = True
        right_was_first = False
        # Loop
        while playing:
            # Clear screen
            self.screen.fill(self.bg_color)
            self.bg_color = (8, 0, 13)
            # Event handling
            playing = self.handle_events()
            # Movement
            self.pos_x, self.pos_y, move_left, move_right, right_was_first = self.read_player_movement(self.pos_x, self.pos_y, move_left, move_right, right_was_first)
            self.move_enemy_towards_player()
            # Rendering
            self.new_enemy()
            self.render_player(self.pos_x, self.pos_y, move_left, move_right)
            self.render_enemies()
            # debugging
            #self.draw_player_hitbox(self.screen)
            #self.draw_enemies_hitbox(self.screen)           
            pygame.draw.rect(self.screen, (40, 36, 43), (0, 0, self.WIDTH, self.HEIGHT * 0.1))
            self.render_lives()
            self.check_kill_collisions()
            self.check_dead_collisions()
            self.show_points()
            self.alive = self.check_player_alive()
            if self.alive == False:
                self.started = False
                return
            # collisions
            #self.check_collisions()
            # Update screen
            pygame.display.flip()
            # Frame rate
            self.clock.tick(60)
        return

    def handle_events(self):
        # Close window event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Esc key event
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                    return False
        return True
    
    # Movement
    def read_player_movement(self, pos_x, pos_y, move_left, move_right, right_was_first):
        # Keyboard input
        keys = pygame.key.get_pressed()
        # From right to left strafe handling
        if not(keys[pygame.K_d]):
            right_was_first = False # Check if right wasn't pressed
        # If both keys are pressed, and right was first, strafe left (right key is being evaluated after,
        # so it was always the first key pressed, so every strafe was to the right)
        if keys[pygame.K_a] and keys[pygame.K_d] and right_was_first:
            # Strafe args
            move_left = True
            move_right = False
            # Up and down movement while strafing left
            if keys[pygame.K_w]:
                pos_y -= self.player_speed
            if keys[pygame.K_s]:
                pos_y += self.player_speed
        # If not strafing left, strafe right (in case is needed), and handle all common movements
        else:
            # Common movements
            if keys[pygame.K_a]:
                pos_x -= self.player_speed if not(keys[pygame.K_w] or keys[pygame.K_s]) else self.player_speed // 1.2
                move_right = False
                move_left = True
            if keys[pygame.K_d]:
                pos_x += self.player_speed if not(keys[pygame.K_w] or keys[pygame.K_s]) else self.player_speed // 1.2
                move_right = True
                move_left = False
                # If right key is pressed and left key is not, right key was first (helper for right strafe)
                if keys[pygame.K_d] and not(keys[pygame.K_a]):
                    right_was_first = True
            # Up and down movement
            if keys[pygame.K_w]:
                pos_y -= self.player_speed if not(keys[pygame.K_a] or keys[pygame.K_d]) else self.player_speed // 1.2
            if keys[pygame.K_s]:
                pos_y += self.player_speed if not(keys[pygame.K_a] or keys[pygame.K_d]) else self.player_speed // 1.2
        return pos_x, pos_y, move_left, move_right, right_was_first
    
    # Enemy Logic
    def move_enemy_towards_player(self):
        for i in range(len(self.enemies)):
            x, y, hitbox = self.enemies[i]
            # Calculate angle towards player
            angle = math.atan2(self.pos_y - y, self.pos_x - x)
            # Move towards player
            x += self.enemy_speed * math.cos(angle)
            y += self.enemy_speed * math.sin(angle)
            self.enemies[i] = (x, y, hitbox)

    def new_enemy(self):
        # Random enemy spawn
        if random.random() <= self.enemy_spawn_chance:
            # Random border spawn
            border = random.choice(["top", "bottom", "left", "right"])
            if border == "top":
                x = random.randint(-150, self.WIDTH)
                y = -150
            elif border == "bottom":
                x = random.randint(-150, self.WIDTH)
                y = self.HEIGHT
            elif border == "left":
                x = -150
                y = random.randint(-150, self.HEIGHT)
            elif border == "right":
                x = self.WIDTH
                y = random.randint(-150, self.HEIGHT)
            self.enemies.append((x, y, self.enemy_hitbox(x, y)))
    
    # Rendering
    def render_enemies(self):
        self.update_enemies_hitbox()
        for enemy in self.enemies:
            self.screen.blit(self.enemy_img, (enemy[0], enemy[1]))

    def render_player(self, pos_x, pos_y, move_left, move_right):
        # Strafe based on horizontal movement
        if move_left:
            player = self.inverted_weapon_img
            self.active_left_hb = True
            self.active_right_hb = False
        elif move_right:
            player = self.weapon_img
            self.active_right_hb = True
            self.active_left_hb = False
        # Player position limits
        self.pos_x = max(0, min(self.WIDTH - player.get_width(), pos_x))
        self.pos_y = max(self.HEIGHT * 0.1, min(self.HEIGHT - player.get_height(), pos_y))
        # Player rendering
        self.screen.blit(player, (self.pos_x, self.pos_y))
        # Player hitbox
        self.update_player_hitbox()
    
    # Hitboxes
    def update_player_hitbox(self):
        # Edge hitboxes
        self.hitbox = pygame.Rect(
            self.pos_x - self.weapon.dims[0] // 30,
            self.pos_y,
            self.weapon.dims[0] - self.weapon.dims[0] // 1.8,
            self.weapon.dims[1] - self.weapon.dims[1] // 3
        )
        self.inverted_hitbox = pygame.Rect(
            self.pos_x + self.hitbox.width * 1.3,
            self.pos_y,
            self.weapon.dims[0] - self.weapon.dims[0] // 1.8,
            self.weapon.dims[1] - self.weapon.dims[1] // 3
        )
        # Stick hitbox to receive damage
        self.stick_hitbox = pygame.Rect(
            self.pos_x + self.weapon.dims[0] // 2.2,
            self.pos_y,
            self.weapon.dims[0] - self.weapon.dims[0] // 1.1,
            self.weapon.dims[1]
        )

    def enemy_hitbox(self, x, y):
        # Enemy hitbox
        return pygame.Rect(
                x + self.enemy.dims[0] * 0.15,
                y + self.enemy.dims[0] * 0.15,
                self.enemy.dims[0] * 0.7,
                self.enemy.dims[1] * 0.7)
    
    def update_enemies_hitbox(self):
        self.enemies_hitbox = []
        for i in range(len(self.enemies)):
            self.enemies[i] = (self.enemies[i][0], self.enemies[i][1], self.enemy_hitbox(self.enemies[i][0], self.enemies[i][1]))
    
    # Debugging
    def draw_enemies_hitbox(self, screen):
        for i in range(len(self.enemies)):
            pygame.draw.rect(screen, (255, 0, 0), self.enemies[i][2], 2)
    def draw_player_hitbox(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        pygame.draw.rect(screen, (0, 255, 0), self.inverted_hitbox, 2)
        pygame.draw.rect(screen, (0, 0, 255), self.stick_hitbox, 2)

    # Collisions
    def check_kill_collisions(self):
        for enemy in self.enemies:
            if (self.hitbox.colliderect(enemy[2]) and self.active_left_hb == True) or (self.inverted_hitbox.colliderect(enemy[2]) and self.active_right_hb == True):
                self.points += self.given_points
                self.enemies.remove(enemy)
                break
    
    def check_dead_collisions(self):
        for enemy in self.enemies:
            if self.stick_hitbox.colliderect(enemy[2]):
                if self.lives > 0:
                    self.lives -= 1
                    self.enemies.remove(enemy)
                    self.flash_screen()
                    break
    
    # Others
    def check_player_alive(self):
        if self.lives == 0:
            return False
        return True
    
    def render_lives(self):
        for i in range(self.lives):
            self.screen.blit(self.full_heart, (self.WIDTH - 100 - (i * 50), 10))
        for i in range(3):
            self.screen.blit(self.empty_heart, (self.WIDTH - 100 - (i * 50), 10))

    def show_points(self):
        font = pygame.font.SysFont('animematrixmben', 36)
        text = font.render(f"Puntos: {self.points}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def flash_screen(self):
        self.bg_color = (53, 26, 74)