import pygame # Pygame is our SDL wrapper
import constants # This module carries the file names and static values

from tiles import Tileset # Our main tileset class
from maps import Map # Each map will be an instance of Map
from state import GameController # Will control the overall state of the game
from state import InputController # Will handle the game input
from player import Player # Will handle the player logic

# Some globals
screen = None
game_controller = None
input_controller = None
main_tileset = None
background_tileset = None
map_level_1 = None
player = None

def setup():
    global screen, game_controller, input_controller, main_tileset, map_level_1, player

    # Initializes pygame
    pygame.init()

    # Initializes the screen
    screen = pygame.display.set_mode(constants.SCREEN_SIZE, pygame.DOUBLEBUF)

    # Initializes the game controllers
    game_controller = GameController()
    input_controller = InputController()

    # Load the sprites
    main_tileset = Tileset(constants.FILEPATH_TILESET_MAIN, constants.TILESIZE)

    # Load the maps
    map_level_1 = Map()
    map_level_1.load_background(constants.FILEPATH_LEVEL1_BACKGROUND, main_tileset)
    map_level_1.load_foreground(constants.FILEPATH_LEVEL1_FOREGROUND, main_tileset)
    map_level_1.load_colliders(constants.FILEPATH_LEVEL1_COLLIDERS, main_tileset)

    # Load the player
    player = Player(constants.FILEPATH_CHARSET)

anchor_x = 0
anchor_y = 0

def game_loop():
    global screen, map_level_1, game_controller, anchor_x, anchor_y, player

    # Enter the main game loop
    while not game_controller.done:

        # Paint the background
        screen.fill((100,200,255))

        # Handle logic
        player.update(map_level_1, anchor_x, anchor_y)

        # Render background and colliders
        map_level_1.background.render(anchor_x, anchor_y, constants.SCREEN_SIZE, screen)
        map_level_1.colliders.render(anchor_x, anchor_y, constants.SCREEN_SIZE, screen)

        # Render player
        player.render(screen)

        # Render Foreground
        map_level_1.foreground.render(anchor_x, anchor_y, constants.SCREEN_SIZE, screen)

        # Check events and look for the exit event
        input()

        # Do the debug
        debug()

        # Update the screen
        pygame.display.flip()


def input():
    global input_controller, game_controller, anchor_x, anchor_y, player

    # Update the input
    input_controller.update()
    
    # Handle events
    if input_controller.quit:
        game_controller.done = True

    if input_controller.left:
        #anchor_x -= 1
        #anchor_x = 0 if anchor_x < 0 else anchor_x
        player.face_left()
        anchor_x, anchor_y = player.walk(anchor_x, anchor_y, 500, left=True)

    if input_controller.right:
        #anchor_x += 1
        player.face_right()
        anchor_x, anchor_y = player.walk(anchor_x, anchor_y, 500, right=True)

    if not (input_controller.right or input_controller.left):
        player.stand()

    if input_controller.up:
        pass

    if input_controller.jump:
        player.start_jump()

    if input_controller.down:
        #anchor_y -= 1
        #anchor_y = 0 if anchor_y < 0 else anchor_y
        pass

def debug():
    global player, anchor_x, anchor_y, screen
    print(player.pos_x, player.pos_y, anchor_x, anchor_y)

    # collisions
    for collision in player.col:
        pygame.draw.rect(screen, pygame.Color(255,0,0), pygame.Rect(*(collision[2])))
        print(collision)


# Run the game setup
setup()

# This is where the game starts
game_loop()