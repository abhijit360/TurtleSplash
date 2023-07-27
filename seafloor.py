import pygame
from pygame.sprite import Sprite

class Seafloor(Sprite):
    def __init__(self,turtlesplash):
        super().__init__()
        self.screen = turtlesplash.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = turtlesplash.settings

        # create a piece of the floor
        self.rect = pygame.Rect((0,0),(self.settings.seabed_width,self.settings.seabed_height))
        self.colour = (0,0,0)
        self.rect.bottom = (self.screen_rect.bottom - 3)

    def update(self):
        self.x = self.rect.x
        self.x -= self.settings.seabed_speed
        self.rect.x = self.x

    def draw_seafloor(self):
        pygame.draw.rect(self.screen,self.colour,self.rect)

