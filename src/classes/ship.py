'''
ship.py class.
'''
import pygame
import os
from classes.laser import Laser, collide

ship_h, ship_w = 100, 150
alien_h, alien_w = 80, 120
# Load images
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_red_small.png")
)
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP, (alien_h, alien_w))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_green_small.png")
)
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP, (alien_h, alien_w))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_blue_small.png")
)
BLUE_SPACE_SHIP = pygame.transform.scale(BLUE_SPACE_SHIP, (alien_h, alien_w))
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_yellow.png")
)
YELLOW_SPACE_SHIP = pygame.transform.scale(YELLOW_SPACE_SHIP, (ship_h, ship_w))
ASTEROID = pygame.image.load(os.path.join("../assets", "asteroid.png"))
ASTEROID = pygame.transform.scale(ASTEROID, (alien_h, alien_w))


WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("../assets", "background-black.png")),
    (WIDTH, HEIGHT),
)

# ... (other images)

# Lasers
RED_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_yellow.png"))


class Ship:
    '''
    This class defines the characteristics of ships within the game world.
    '''
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    '''
    This class defines the characteristics of the player's ship.
    '''
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width(),
                10,
            ),
        )
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width() * (self.health / self.max_health),
                10,
            ),
        )


class Enemy(Ship):
    '''
    This class defines the characteristics of the enemy's ship.
    '''
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Asteroid(Ship):
    '''
    This class defines the characteristics of asteroids that appear within the game world.
    '''
    COLOR_MAP = {
        "asteroid": ASTEROID,
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel