import pygame

class Hungerbar():
    def __init__(self,TS):
        # obtain an attribute of the display surface
        self.screen = TS.screen

        # actual hunger bar
        self.hungerbar_width , self.hungerbar_height = 50,10
        self.hungerbar = pygame.Rect((130,5),(self.hungerbar_width,self.hungerbar_height))

        # flags to check if turtle has eaten
        self.starving = True

        # time stamps to use to decrease hunger in a set period of time
        self.time_stamp = TS.start_time


    def update(self):

        if self.starving and (pygame.time.get_ticks()- self.time_stamp) > 1500:
            """checks if turtle is starving. Using the starting game timestamp, pygame.time.get_ticks()- self.time_stamp
            checks for a delay of 1.5 seconds before decreasing food bar by 20%"""
            self.hungerbar.width -= 5
            self.time_stamp = pygame.time.get_ticks() # resets the time stamp to continue


    def display_hunger(self):
        # generate font to use for hungerbar
        font = pygame.font.Font("freesansbold.ttf", 15)
        message = font.render(f"Hunger:", False, (0, 0, 0))
        message_rect = message.get_rect()
        message_rect.topleft = (70,0)

        self.screen.blit(message,message_rect)

        self.screen.fill((15, 117, 15),self.hungerbar)
