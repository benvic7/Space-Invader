import pygame
import os
import random

from Enemy import Enemy
from Laser import collide
from Player import Player

# initializing font
pygame.font.init()

# creating our window/background
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))


# main loop running the game
def main():
    run = True  # while True, the game will run
    clock = pygame.time.Clock()  # creating a clock object
    FPS = 60  # defining our frames per second

    main_font = pygame.font.SysFont("courier", 30)
    lost_font = pygame.font.SysFont("courier", 60)

    lost = False
    lost_count = 0
    level = 0
    lives = 5

    enemies = []  # enemy dictionary
    player = Player(300, 650)  # player object
    wave_length = 5  # every level we generate a new wave (5 new enemies)

    enemy_vel = 1  # enemy speed
    player_vel = 10  # player speed
    enemy_laser_vel = 10  # enemy laser speed
    user_laser_vel = 15  # player laser speed

    # we redraw the screen 60 times per second (based on our FPS rate)
    def redraw_window():
        # drawing the background
        WIN.blit(BG, (0, 0))

        # drawing the lives and level text labels
        lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # drawing the enemy
        for enemy in enemies:
            enemy.draw(WIN)

        # drawing the player
        player.draw(WIN)

        # drawing the "You lost!" screen if the player loses
        if lost:
            lost_label = lost_font.render("You lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        # updates the display 60 times per second
        pygame.display.update()

    # this is our main while loop that keeps the game running
    while run:
        clock.tick(FPS)  # ensures the clock ticks 60 times per second
        redraw_window()  # redrawing the screen

        # if we have lost, set lost to true and lost count to 1
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        # when we lose, our lost message will appear for 3 seconds, then the game will exit
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
                # generate a random enemy at a random point above the screen
                enemy = Enemy(random.randrange(100, WIDTH - 100), random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # check for an event every clock cycle. If the event is quit, stop the loop.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # checking to see what keys are pressed
        keys = pygame.key.get_pressed()

        # LEFT key
        if keys[pygame.K_LEFT] and (player.x - player_vel > 0):
            player.x -= player_vel
        # RIGHT key
        if keys[pygame.K_RIGHT] and (player.x + player_vel + player.get_width() < WIDTH):
            player.x += player_vel
        # UP key
        if keys[pygame.K_UP] and (player.y - player_vel > 0):
            player.y -= player_vel
        # DOWN key
        if keys[pygame.K_DOWN] and (player.y + player_vel + player.get_height() + 10 < HEIGHT):
            player.y += player_vel
        # SHOOT key
        if keys[pygame.K_SPACE]:
            player.shoot()

        # enemy loop
        for enemy in enemies[:]:
            # moving the enemy and enemy lasers
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            # 50% chance of the enemy shooting every 3 seconds
            if random.randrange(0, 3 * 60) == 1:
                enemy.shoot()

            # if we collide with the enemy, it should remove the enemy ship and some of our health
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            # else if the enemy got past us, delete the enemy and remove a life
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        # move lasers if we shoot
        player.move_lasers(-user_laser_vel, enemies)


# function for our main menu
def main_menu():
    title_font = pygame.font.SysFont("courier", 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()

        # if we press the quit button, quit the game. If we press any other key, start the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


main_menu()
