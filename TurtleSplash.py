import pygame, sys , random , json

from settings import Settings
from turtle import Turtle
from Sandfloor import Sandbed
from seafloor import Seafloor
from cup import Cup
from plastic_bottle import PlasticBottle
from seaweed import Seaweed
from hunger_bar import Hungerbar
from homepage import Homepage
from endpage import Endpage

class TurtleSplash:
    def __init__(self):
        ''' configure the pygame module and the game class'''
        pygame.init()
        self.clock = pygame.time.Clock()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))

        self.turtle = Turtle(self)

        #create groups to deal with sand and sea bed
        self.sandfloor = pygame.sprite.Group()
        self.seafloor = pygame.sprite.Group()

        self.floor_units = self.settings.screen_width // (self.settings.seabed_width * 2)

        # create a group to deal with all the trash sprites
        self.trash = pygame.sprite.Group()

        # create a group to deal with seaweed sprites
        self.seaweed = pygame.sprite.Group()

        # keep track of seaweed / trash eaten
        self.seaweed_eaten = 0
        self.trash_eaten = 0

        # to check if turtle is suffocating/ eaten trash
        self.is_chocking = False
        self.start_chocking = 0 # this variable helps to time chocking period

        # time stamp to use as a constant value once game has begun
        self.start_time = pygame.time.get_ticks()

        # hunger bar
        self.hungerbar = Hungerbar(self)

        self.score_file = "score_file.json" # store the score

        # homepage object
        self.homepage = Homepage(self)

        # endpage object
        self.endpage = Endpage(self)




    def run_game(self):
        """ The loop that runs the game"""
        while True:
            # displays the homepage and checks if the player wants to start game
            while not self.homepage.is_running and not self.endpage.endscreen_display:
                self.homepage.getscore()
                self.homepage.homepage_display()
                self.homepage.start_game()

                # reset the death flags and score
                self.endpage.suffocated = False
                self.endpage.starved = False
                self.trash_eaten = 0
                self.is_chocking = False
                self.homepage.score = 0


                self.hungerbar.hungerbar.width = self.hungerbar.hungerbar_width

            while self.endpage.endscreen_display:
                self.endpage.endpage_display()
                self.endpage.restart_game()



            while self.homepage.is_running == True and self.endpage.endscreen_display == False:
                self.clock.tick(60)  # runs the game at 60 frames per second
                self._check_events()
                self.turtle.move()

                self._manage_sea_floor()
                self.seafloor.update()

                self._manage_sand_floor()
                self.sandfloor.update()

                self._manage_trash()
                self.trash.update()

                self._manage_seaweed()
                self.seaweed.update()

                self._check_trash_eaten()
                self._check_seaweed_eaten()

                self.hungerbar.update()

                self._end_game()
                self._update_screen()


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._store_score()
                self.homepage.is_running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.turtle.moving_down = True
                if event.key == pygame.K_UP:
                    self.turtle.moving_up = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.turtle.moving_down = False
                if event.key == pygame.K_UP:
                    self.turtle.moving_up = False

    def _update_screen(self):
        self.screen.fill(self.settings.bg_colour)
        self.turtle.blitme()
        for f in self.seafloor.sprites():
            f.draw_seafloor()
        for s in self.sandfloor.sprites():
            s.drawme()
        self.trash.draw(self.screen)
        self.seaweed.draw(self.screen)
        self._display_points()
        self._display_chocking()
        self.hungerbar.display_hunger()

        pygame.display.flip()


    def _generate_sea_floor(self):
        for i in range(self.floor_units):
            unit = Seafloor(self)
            unit.rect.x = self.settings.screen_width + self.settings.seabed_width * 2 * i
            self.seafloor.add(unit)


    def _generate_sand_floor(self):
        for i in range(self.floor_units//20):
            # places one every  floor units
            unit = Sandbed(self)
            unit.sand_rect.x =self.settings.screen_width
            self.sandfloor.add(unit)

    def _generate_trash(self):
        trashtype = random.choice(["c", "b"])
        if trashtype == "c":
            trash = Cup(self)
            self.trash.add(trash)
        elif trashtype == 'b':
            trash = PlasticBottle(self)
            self.trash.add(trash)

    def _manage_sea_floor(self):
        # generate and delete sprite once off the screen
        if not self.seafloor or len(self.seafloor) < self.floor_units:
            self._generate_sea_floor()

        for f in self.seafloor.sprites():
            if f.rect.x <= 0:
                self.seafloor.remove(f)

    def _manage_sand_floor(self):
        # generate and delete sprite once off the screen
        if not self.sandfloor or len(self.sandfloor) < self.floor_units / 10:
            self._generate_sand_floor()

        for s in self.sandfloor.sprites():
            if s.sand_rect.x <= 0:
                self.sandfloor.remove(s)

    def _manage_trash(self):
        # generate and delete trash once off the screen
        # runs generate trash at the start when self.trash is empty, and keeps producing sprites as long as there are
        # fewer than 5
        if not self.trash or len(self.trash) < self.settings.trash_amt:
            self._generate_trash()

        for t in self.trash.sprites():
            if t.rect.x < 0:
                self.trash.remove(t)

    def _generate_seaweed(self):
        sw = Seaweed(self)
        self.seaweed.add(sw)

    def _manage_seaweed(self):
        if not self.seaweed or len(self.seaweed) < 5:
            self._generate_seaweed()

        for sw in self.seaweed.sprites():
            if sw.rect.x < 0:
                self.seaweed.remove(sw)

    def _check_trash_eaten(self):
        for t in self.trash.sprites():
            if pygame.sprite.collide_rect(t, self.turtle):
                self.trash.remove(t)
                self.start_chocking = pygame.time.get_ticks()
                self.is_chocking = True
                self.trash_eaten += 1


        if pygame.time.get_ticks() - self.start_chocking > 5000:
            self.is_chocking = False
            # turtle dies of suffocation only if another piece of trash is eaten while chocking
            self.trash_eaten = 0

    def _display_chocking(self):
        # prints chocking if trash eating
        font = pygame.font.Font("freesansbold.ttf", 32)
        message = font.render(f"CHOCKING",False,(255,0,0))
        message_rect = message.get_rect()
        message_rect.x = self.settings.screen_width // 2 - 30
        if self.is_chocking:
            self.screen.blit(message,message_rect)

    def _check_seaweed_eaten(self):
        time_eaten = 0
        for sw in self.seaweed.sprites():
            if pygame.sprite.collide_rect(sw, self.turtle) and not self.is_chocking:
                self.seaweed_eaten += 1
                self.seaweed.remove(sw)
                time_eaten = pygame.time.get_ticks()
                self.hungerbar.starving = False
                if self.hungerbar.hungerbar.width < self.hungerbar.hungerbar_width:
                    # limits the hunger bar from increasing past the original length
                    self.hungerbar.hungerbar.width += 10

        if pygame.time.get_ticks() - time_eaten > 1500:
            # resets starving back to true
            self.hungerbar.starving = True

    def _display_points(self):
        font = pygame.font.Font("freesansbold.ttf",15)
        message = font.render(f"Score :{self.seaweed_eaten}",False,(0,0,0))
        message_rect = message.get_rect()
        message_rect.topleft = (0 , 0)
        self.screen.blit(message,message_rect)

    def _store_score(self):
        with open(self.score_file,'w') as sf:
            json.dump(self.seaweed_eaten,sf)

    def _end_game(self):
        # method that checks for events/ situations where the game ends
        if self.hungerbar.hungerbar.width <= 0:
            print(self.hungerbar.hungerbar_width)
            # dies of starvation if hunger bar drops to zero
            self._store_score()
            self.homepage.is_running = False
            self.endpage.starved = True
            self.endpage.endscreen_display = True

        if self.trash_eaten > 1:
            # dies of suffocation if more than 2 piece of trash are eaten
            self._store_score()
            self.homepage.is_running = False
            self.endpage.suffocated = True
            self.endpage.endscreen_display = True

if __name__ == "__main__":
    ts = TurtleSplash()
    ts.run_game()