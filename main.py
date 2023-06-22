import pygame
import os
import random

from Enemy import Enemy
from Player import Player

pygame.font.init()

# creating our window/background
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader Tutorial")

# LOAD IMAGES

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))

# laser class
# ship class
# player ship class (extension of ship)
# enemy ship class (extension of ship)

# THE FOLLOWING FUNCTIONS ARE OUTSIDE OF A CLASS

# Both objects have a mask. If the masks are overlapping based on the offset we have given them
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x      # distance between object 1 and object 2 (horizontally)
    offset_y = obj2.y - obj1.y      # distance between object 1 and object 2 (vertically)
    # if not overlapping, we will return 1. If we are overlapping, we will return a touple of (x, y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

# MAIN LOOP
def main():
    # initializing variables
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("courier", 50)
    lost_font = pygame.font.SysFont("courier", 60)

    enemies = []
    wave_length = 5     # every level we generate a new wave
    enemy_vel = 1       # enemy speed

    player_vel = 5      # every time a user presses a key, it moves 5 pixels
    laser_vel = 5

    # player object
    player = Player(300, 650)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    # we redraw the screen based on our FPS rate (60 times per second?)
    def redraw_window():
        WIN.blit(BG, (0,0))     # placing in our background

        # drawing our lives and level text labels
        lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # drawing the enemy (behind the player)
        for enemy in enemies:
            enemy.draw(WIN)

        # drawing the player
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    # MAIN LOOP
    while run:
        clock.tick(FPS)     # ticking our clock based on our FPS rate (60)
        redraw_window()     # redrawing the screen

        # If we have lost, set lost to true and lost count to 1
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        # When we lose, our lost message will appear for 3 seconds, then the game will exit
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # if we have killed all the enemies, increase the level by 1 and number of enemies by 5
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():        # check for an event every clock cycle
            if event.type == pygame.QUIT:       # if we press the quit button, loop will fail
                quit()

        # checking to see what keys are pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and (player.x - player_vel > 0): # left KEY
            player.x -= player_vel
        if keys[pygame.K_d] and (player.x + player_vel + player.get_width() < WIDTH): # right KEY
            player.x += player_vel
        if keys[pygame.K_w] and (player.y - player_vel > 0): # up KEY
            player.y -= player_vel
        if keys[pygame.K_s] and (player.y + player_vel + player.get_height() + 10 < HEIGHT): # down KEY
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 3*60) == 1:       # 50% chance of a shot every 3 seconds (60 fps, between 1 and 2)
                enemy.shoot()

            # if we collide with the enemy, it should remove the enemy and our ship
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                # removing enemies from the list copy so that when we are at 0 enemies we can advance levels
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("courier", 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        # if we press the quit button, quit the game. If we press any other key, start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()

main_menu()