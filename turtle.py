import pygame

class Turtle:
    def __init__(self,turtlesplash):

        self.screen = turtlesplash.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = turtlesplash.settings


        self.image = pygame.image.load("turtle.png")
        self.rect = self.image.get_rect()

        # position turtle left side of display
        self.rect.left = (self.screen_rect.left + 10)

        # movement flags
        self.moving_up = False
        self.moving_down = False
        self.speed = self.settings.turtle_speed

    def blitme(self):
        self.screen.blit(self.image,self.rect)


    def move(self):
        """ Proviedes continuous movement through movement flags. This method is called every frame giving an impression
         of continuous movement"""

        if self.moving_up and self.rect.top > 0:
            self.y = self.rect.y
            self.y -= self.speed
            self.rect.y = self.y
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom - 56:
            self.y = self.rect.y
            self.y += self.speed
            self.rect.y = self.y





