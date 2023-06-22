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
USER_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# lasers
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))

# laser class
class Laser:
    # constructor to initialize the laser
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # method to draw the laser
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # method to move the laser
    def move(self, vel):
        self.y += vel

    # method to tell us if the laser is off the screen
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    # method to tell us if the laser collides with an object (ship)
    def collision(self, obj):
        return collide(obj, self)

# ship class
class Ship:
    COOLDOWN = 30
    # constructor to initialize ships
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None            # draw the ship
        self.laser_img = None           # draw the laser
        self.lasers = []
        self.cool_down_counter = 0

    # method to draw ships
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # method to move lasers
    def move_lasers(self, vel, obj):
        self.cooldown()     # call the cooldown so we can't shoot too fast
        for laser in self.lasers:
            laser.move(vel)     # will continue to move if on screen and not colliding
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)       # remove laser if off screen
            elif laser.collision(obj):
                obj.health -= 10        # decrease enemy health if collision
                self.lasers.remove(laser)       # remove laser if collision

    # laser cool down method
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # method to shoot lasers
    def shoot(self):
        if self.cool_down_counter == 0:     # if we're not in the cooldown stage of waiting to shoot the next laser
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # returns ship width
    def get_width(self):
        return self.ship_img.get_height()

    # returns ship height
    def get_height(self):
        return self.ship_img.get_width()

# player ship class (extension of ship)
class Player(Ship):
    # player ship constructor
    def __init__(self, x, y, health = 100):
        # Using ships initialization method on player
        super().__init__(x, y, health)
        self.ship_img = USER_SHIP
        self.laser_img = YELLOW_LASER
        # Creates a mask of the image (so we can do pixel-perfect collision)
        self.mask = pygame.mask.from_surface(USER_SHIP)
        self.max_health = health

    # method to move player lasers
    def move_lasers(self, vel, objs):
        self.cooldown()     # call the cooldown so we can't shoot too fast
        for laser in self.lasers:
            laser.move(vel)     # will continue to move if on screen and not colliding
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)       # remove laser if off-screen
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)        # remove the object (what is the object) if the laser has collided with it
                        if laser in self.lasers:
                            self.lasers.remove(laser)       # remove laser if collision

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        # drawing a red and green rectangle for the health bars rect(surface, color, (height, width))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        # multiplying the width by current health/max health to get the percentage of health we have left
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


# enemy ship class (extension of ship)
class Enemy(Ship):
    # dictionary of ships
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }

    # enemy ship constructor
    def __init__(self, x, y, color, health = 100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # method to move enemy ship (CHANGE THIS IN FINAL)
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:     # if we're not in the cooldown stage of waiting to shoot the next laser
            # can alter this if I want it to be more centered shooting
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

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