import pygame


# collide function
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x  # distance between object 1 and object 2 (horizontally)
    offset_y = obj2.y - obj1.y  # distance between object 1 and object 2 (vertically)
    # if not overlapping, we will return 1. If we are overlapping, we will return a touple of (x, y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


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