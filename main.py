import pygame
import os
import time
import random
pygame.font.init()

# creating our window/background
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader Tutorial")

# LOAD IMAGES
# enemy ships
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))

# user ship
USER_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow_small.png"))

# lasers
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))

# ship constructor
class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.player_img = None            # draw the ship
        self.laser_img = None           # draw the laser
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))

class Player(Ship):
    def __init__(self, x, y, health = 100):
        # Using ships initialization method on player
        super().__init__(x, y, health)
        self.player_img = USER_SHIP
        self.laser_img = YELLOW_LASER
        # Creates a mask of the image (so we can do pixel-perfect collision)
        self.mask = pygame.mask.from_surface(self.player_img)
        self.max_health = health

# MAIN LOOP
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("courier", 50)

    player_vel = 5      # every time a user presses a key, it moves 5 pixels

    # player object
    player = Player(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))     #placing in our background

        # drawing our lives and level text labels
        lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # drawing the player
        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)     # ticking our clock based on our FPS rate (60)
        redraw_window()

        for event in pygame.event.get():        # check for an event every clock cycle
            if event.type == pygame.QUIT:       # if we press the quit button, loop will fail
                run = False

        # checking to see what keys are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and (player.x - player_vel > 0): # left KEY
            player.x -= player_vel
        if keys[pygame.K_d] and (player.x + player_vel + 50 < WIDTH): # right KEY
            player.x += player_vel
        if keys[pygame.K_w] and (player.y - player_vel > 0): # up KEY
            player.y -= player_vel
        if keys[pygame.K_s] and (player.y + player_vel + 50 < HEIGHT): # down KEY
            player.y += player_vel


main()