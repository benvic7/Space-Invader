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
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "red_ship.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "green_ship.png"))
PURPLE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "purple_ship.png"))

# user ship
USER_SHIP = pygame.image.load(os.path.join("assets", "user_ship.png"))

#laser
LASER = pygame.image.load(os.path.join("assets", "laser.png"))

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))

# ship constructor
class Ship:
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None            # draw the ship
        self.laser_img = None           # draw the laser
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))

# MAIN LOOP
def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("courier", 50)

    player_vel = 5      # every time a user presses a key, it moves 5 pixels

    # ship object
    ship = Ship(300, 650)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0,0))     #placing in our background

        # drawing our lives and level text labels
        lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # drawing the ship
        ship.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)     # ticking our clock based on our FPS rate (60)
        redraw_window()

        for event in pygame.event.get():        # check for an event every clock cycle
            if event.type == pygame.QUIT:       # if we press the quit button, loop will fail
                run = False

        # checking to see what keys are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: # left KEY
            ship.x -= player_vel
        if keys[pygame.K_d]: # right KEY
            ship.x += player_vel
        if keys[pygame.K_w]: # up KEY
            ship.y -= player_vel
        if keys[pygame.K_s]: # down KEY
            ship.y += player_vel


main()