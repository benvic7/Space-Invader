from Laser import Laser

# defining the width and height of our screen
WIDTH, HEIGHT = 750, 750


class Ship:
    COOLDOWN = 30

    # constructor to initialize ships
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None  # draw the ship
        self.laser_img = None  # draw the laser
        self.lasers = []
        self.cool_down_counter = 0

    # method to draw ships
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # method to move lasers
    def move_lasers(self, vel, obj):
        self.cooldown()  # call the cooldown so we can't shoot too fast
        for laser in self.lasers:
            laser.move(vel)  # will continue to move if on screen and not colliding
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)  # remove laser if off-screen
            elif laser.collision(obj):
                obj.health -= 10  # decrease enemy health if collision
                self.lasers.remove(laser)  # remove laser if collision

    # laser cool down method
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # method to shoot lasers
    def shoot(self):
        if self.cool_down_counter == 0:  # if we're not in the cooldown stage of waiting to shoot the next laser
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # returns ship width
    def get_width(self):
        return self.ship_img.get_height()

    # returns ship height
    def get_height(self):
        return self.ship_img.get_width()
