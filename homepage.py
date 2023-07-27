import pygame , json , sys

class Homepage():
    def __init__(self,TS):
        self.screen = TS.screen
        self.settings = TS.settings

        #generate welcome font and render welcome message
        self.welcome_font = pygame.font.SysFont("",45)
        self.welcome_message = self.welcome_font.render("TURTLE SPLASH",False,(98, 252, 3))

        # generate instruction font and render instructions
        self.font =pygame.font.SysFont("", 24)
        self.instructions1 = self.font.render("Eat Seaweed to stay alive!",False,(98, 252, 3))
        self.instructions2 = self.font.render("Avoid garbage as they are a chocking hazard",False, (98, 252, 3))
        self.instructions3= self.font.render("Press SPACE to start", False, (98, 252, 3))

        # create message of previous score
        self.file = "score_file.json"
        self.score = 0

        #flag to check if game has begun
        self.is_running = False

    def getscore(self):
        with open(self.file,'r') as f:
            self.score = json.load(f)
            self.score_message = self.font.render(f"Score to beat:{self.score}", False, (98, 252, 3))

    def homepage_display(self):
        # gives the homescreen a solid background colour
        self.screen.fill(self.settings.bg_colour)
        # draws the messages at their individual positions
        self.screen.blit(self.welcome_message,(60,160))
        self.screen.blit(self.instructions1, (60,210))
        self.screen.blit(self.instructions2, (60,230))
        self.screen.blit(self.instructions3, (60,250))
        self.screen.blit(self.score_message, (60,270))

        pygame.display.flip()

    def start_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_running = True

