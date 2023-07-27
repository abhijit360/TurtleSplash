import pygame, random
from pygame.sprite import Sprite

class Seaweed(Sprite):
    def __init__(self, TS):
        super().__init__()

        # create a display attribute and a settings attribute
        self.screen = TS.screen
        self.settings = TS.settings

        # load image and create a rect
        self.image = pygame.image.load("seaweed.png")
        self.rect = self.image.get_rect()

        # randomise the y co-ordinate and set the sprite at the edge of the right screen
        self.rect.y = random.randint(0, (self.settings.screen_height - 80 ))
        self.rect.x = self.settings.screen_width

        # trash settings
        # gives a sense of randomness to the speed of the trash
        self.speed = random.choice([1,2])

    def update(self):
        # moves the trash to the left at set speed
        self.x = self.rect.x
        self.x -= self.speed
        self.rect.x = self.x