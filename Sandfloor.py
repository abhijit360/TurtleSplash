import pygame
from pygame.sprite import Sprite

class Sandbed(Sprite):

    def __init__(self,turtle_splash):
        super().__init__()

        self.screen = turtle_splash.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = turtle_splash.settings

        self.sand_image = pygame.image.load("sand.png")
        self.sand_rect = self.sand_image.get_rect()

        self.sand_rect.bottom = (self.screen_rect.bottom - 5)


    def update(self):
        self.x = self.sand_rect.x
        self.x -= self.settings.seabed_speed
        self.sand_rect.x = self.x


    def drawme(self):
        self.screen.blit(self.sand_image,self.sand_rect)