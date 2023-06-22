import pygame
import os
from Ship import Ship

WIDTH, HEIGHT = 750, 750

USER_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
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

