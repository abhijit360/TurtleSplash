import pygame, sys

class Endpage():
    def __init__(self,TS):
        self.screen = TS.screen
        self.settings = TS.settings
        self.homepage = TS.homepage

        #generate end screen font and render end message
        self.welcome_font = pygame.font.SysFont("",45)
        self.Endscreen_message = self.welcome_font.render("GAME OVER!", False, (98, 252, 3))

        # generate death cause font ,death cause message, restart game message
        self.font =pygame.font.SysFont("", 32)
        self.suffocation_msg = self.font.render("Suffocated on garbage ",False,(98, 252, 3))
        self.starvation_msg = self.font.render("Died of starvation",False, (98, 252, 3))
        self.restart_msg = self.font.render("press 'r' to try again!",False,(98,252,3))


        # flags to check cause of death to display correct message
        self.starved = False
        self.suffocated = False

        # flag to display
        self.endscreen_display = False




    def endpage_display(self):
        # gives the homescreen a solid background colour
        self.screen.fill(self.settings.bg_colour)
        # draws the messages at their individual positions
        self.screen.blit(self.Endscreen_message, (60, 160))
        self.screen.blit(self.restart_msg,(60,200))

        # check cause of death and display death message
        if self.starved:
            self.screen.blit(self.starvation_msg,(60,250))
        if self.suffocated:
            self.screen.blit(self.suffocation_msg,(60,250))

        pygame.display.flip()

    def restart_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.homepage.is_running = False
                    self.endscreen_display = False



