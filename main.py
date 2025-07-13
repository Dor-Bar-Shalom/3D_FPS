import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from renderingEngine import *
# from spriteEntity import *
from entityManager import *
from weapon import *
from sound import *
from graphNavigator import *
WHITE = pg.Color('white')
BLACK = pg.Color('black')
GREY = pg.Color('grey')

# Represents the main game class responsible for managing the game loop and game elements.
class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.event.set_grab(True)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.sound = Sound(self)
        pg.mixer.music.play(-2)
        self.map_choice = None
        self.mapSelection()
        self.difficulty_choice = None;
        self.difficultySelection()


    # Displays a map selection screen and allows the user to choose a map.
    def mapSelection(self):
        # Define font and size
        font = pg.font.SysFont('comicsansms', 50)
        text = font.render('Choose a map', True, WHITE)
        background_image = pg.image.load("resources\opening.png")
        self.screen.blit(background_image, (0, 0))
        # Define button size and position
        button_width = 200
        button_height = 50
        button_margin = 50
        button_x = (WIDTH - button_width) // 2
        button_y1 = HEIGHT // 2 - button_margin
        button_y2 = HEIGHT // 2 + button_margin

        # Create buttons
        button1 = pg.Rect(button_x, button_y1, button_width, button_height)
        button2 = pg.Rect(button_x, button_y2, button_width, button_height)
        current_button = 1

        while self.map_choice is None:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        current_button = 1
                    elif event.key == pg.K_DOWN:
                        current_button = 2
                    elif event.key == pg.K_RETURN:
                        if current_button == 1:
                            self.map_choice = 1
                        elif current_button == 2:
                            self.map_choice = 2

            # Draw buttons and text on the screen
            pg.draw.rect(self.screen, WHITE, button1 if current_button == 1 else button2)
            pg.draw.rect(self.screen, BLACK, button2 if current_button == 1 else button1)
            self.screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 4))
            font = pg.font.SysFont('comicsansms', 30)
            button1_text = font.render('Map 1', True, GREY)
            button2_text = font.render('Map 2', True, GREY)
            self.screen.blit(button1_text, (button_x + (button_width - button1_text.get_width()) // 2,
                                            button_y1 + (button_height - button1_text.get_height()) // 2))
            self.screen.blit(button2_text, (button_x + (button_width - button2_text.get_width()) // 2,
                                            button_y2 + (button_height - button2_text.get_height()) // 2))
            pg.display.update()


    # Displays a difficulty selection screen and allows the user to choose a difficulty level.
    def difficultySelection(self):
        # define image
        background_image = pg.image.load("resources\opening.png")
        self.screen.blit(background_image, (0, 0))
        # Define font and size
        font = pg.font.SysFont('comicsansms', 50)
        text = font.render('Choose a difficulty', True, WHITE)

        # Define button size and position
        button_width = 200
        button_height = 50
        button_margin = 50
        button_x = (WIDTH - button_width) // 2
        button_y1 = HEIGHT // 2 - button_margin
        button_y2 = HEIGHT // 2 + button_margin

        # Create buttons
        button1 = pg.Rect(button_x, button_y1, button_width, button_height)
        button2 = pg.Rect(button_x, button_y2, button_width, button_height)
        current_button = 1

        while self.difficulty_choice is None:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        current_button = 1
                    elif event.key == pg.K_DOWN:
                        current_button = 2
                    elif event.key == pg.K_RETURN:
                        if current_button == 1:
                            self.difficulty_choice = 1
                        elif current_button == 2:
                            self.difficulty_choice = 2

            # Draw buttons and text on the screen
            pg.draw.rect(self.screen, WHITE, button1 if current_button == 1 else button2)
            pg.draw.rect(self.screen, BLACK, button2 if current_button == 1 else button1)
            self.screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 4))
            font = pg.font.SysFont('comicsansms', 30)
            button1_text = font.render('Easy', True, GREY)
            button2_text = font.render('Hard', True, GREY)
            self.screen.blit(button1_text, (button_x + (button_width - button1_text.get_width()) // 2,
                                            button_y1 + (button_height - button1_text.get_height()) // 2))
            self.screen.blit(button2_text, (button_x + (button_width - button2_text.get_width()) // 2,
                                            button_y2 + (button_height - button2_text.get_height()) // 2))
            pg.display.update()

        # Once a difficulty is chosen, start the game
        self.new_game(self.map_choice, self.difficulty_choice)

    # Starts a new game with the selected map and difficulty level.
    def new_game(self, map_choice,difficulty_choice):
        # self.sound = Sound(self)
        # pg.mixer.music.play(-1)
        self.map_choice = map_choice
        self.map = Map(self,map_choice)
        self.player = Player(self)
        self.object_renderer = RenderingEngine(self)
        self.raycasting = RayCasting(self)
        self.difficulty_choice = difficulty_choice
        self.entity_manager = EntityManager(self, difficulty_choice)
        self.weapon = Weapon(self)
        self.pathfinding = GraphNavigator(self)


    # Updates the game elements and handles the game logic.
    def update(self):
        cross_sight = pg.image.load("resources\cross.png")
        self.screen.blit(cross_sight, (775, 450))
        self.player.update()
        self.raycasting.update()
        self.entity_manager.update()
        self.weapon.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    # Draws the game elements on the screen.
    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        # self.map.draw()
        # self.player.draw()

    # Checks for various events, such as quitting the game or key presses.
    def checkEvents(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    # Runs the game loop.
    def run(self):
        while True:
            self.checkEvents()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
