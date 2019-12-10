"""
This module has all information used to handle the player, including the player
class and the constants used to control the player state.
"""

import pygame

from maps import Map
from collisions import *

import constants

class PlayerState:
    """
    The PlayerState class has many attributes that represent states the player
    can assume. Usually it is better to use a integer for quick testing when
    defining such constants, but in this case they have been set as strings to
    make debugging and comprehension easier.
    """

    # Action state constants
    STANDING = 'standing'
    WALKING = 'walking'
    JUMPING = 'jumping'
    CROUCHING = 'crouching'

    # Ground state constants
    GROUNDED = 'grounded'
    AIR = 'air'

    # Direction state constants
    LEFT = 'left'
    RIGHT = 'right'

class Player:
    """
    This class represents a player in the game world. It carries all the logic
    of the player as well as its attributes. That shows a typical example of
    encapsulation, where we have all the data from the player encapsulated
    inside the class alongside with the methods that manipulate this data.
    The idea is to delegate to this class all logic behind the player and just
    use the methods like walk(), jump() and update() as facades to the more
    complex code that has to be executed.
    The player works based on states. Those states will define what actions can
    be done and to what state the player will move next. The state also defines
    what animation frames are going to be used.
    """

    def __init__(self, filename: str):

        self.col = []

        # The player frames are stored in dictionaries. To make things simpler,
        # we have a dictionary for each direction as the player can face left
        # or right.
        self.sprites_right = {}
        self.sprites_left = {}

        # Those counters will store the current frame and the frame ticks. As
        # by default the game will run too quick, we need to wat a little bit
        # in betwen frames. Each game frame will count a tick. Every x ticks
        # the frame will be updated.
        self.current_frame = 0
        self.ticks = 0

        # Set the initial states of the player
        self.current_state = PlayerState.STANDING
        self.ground_state = PlayerState.AIR
        self.direction = PlayerState.RIGHT

        # X and Y positions in the screen.
        self.pos_x = 0
        self.pos_y = 0

        self.player_speed = 0.5
        self.gravity_speed = 0.9

        # The current jump is a variable that is always used when applying
        # gravity. It should be decreased each frame until it reaches zero. The
        # jump_speed will define how much force will be applied initially so
        # that the player moves upwards.
        self.current_jump = 0
        self.jump_speed = -3

        # Instantiate the player boundaries.
        self.boundaries = BoundingBox(constants.PLAYER_SIZE, constants.PLAYER_SIZE)

        # Load the sprites
        self.__load_sprites(filename)

    def __load_sprites(self, filename:str):
        """
        Will load the player sprites.
        """
        # Initialize some variables
        sprites_right = []
        sprites_left = []
        
        # Load the full spritesheet images
        full_spritesheet_right = pygame.image.load(filename)
        full_spritesheet_left = pygame.transform.flip(full_spritesheet_right, True, False)

        # Here we count how many sprites we have in the image both in the X and Y
        # axis.
        size_x = int(full_spritesheet_right.get_width()/constants.PLAYER_SIZE)
        size_y = int(full_spritesheet_right.get_height()/constants.PLAYER_SIZE)

        # Go over the X and Y dimensions and start chopping the image
        # Here we have two lists (sprites_right and sprites_left) that will store
        # our animation frames. We need to create a new surface with the size
        # of the file and then draw the region of the spretesheet that we want
        # into that surface we created. This surfaces is then stored inside the
        # list and then later used to render the character.
        for x in range(0, size_x):
            for y in range(0, size_y):
                
                # Slice the image for the Right sprite
                new_tile = pygame.Surface((constants.PLAYER_SIZE, constants.PLAYER_SIZE), pygame.SRCALPHA)
                new_tile.blit(full_spritesheet_right, (0,0), (x*constants.PLAYER_SIZE, y*constants.PLAYER_SIZE, constants.PLAYER_SIZE, constants.PLAYER_SIZE))
                sprites_right.append(new_tile)

                # Slice the image for the Left sprite
                new_tile = pygame.Surface((constants.PLAYER_SIZE, constants.PLAYER_SIZE), pygame.SRCALPHA)
                new_tile.blit(full_spritesheet_left, (0,0), (x*constants.PLAYER_SIZE, y*constants.PLAYER_SIZE, constants.PLAYER_SIZE, constants.PLAYER_SIZE))
                sprites_left.append(new_tile)

        # Assign the sprites to the actions
        # As the sprites facing left are based on the flipped image, the
        # coordinates are different.
        # For each state we add an entry in the dictionary with the state we
        # want.

        # So below, just a bunch of variable assignments
        self.sprites_right['standing'] = []
        self.sprites_left['standing'] = []
        self.sprites_right['standing'].append(sprites_right[0])
        self.sprites_left['standing'].append(sprites_left[6])

        self.sprites_right['walking'] = []
        self.sprites_left['walking'] = []
        for i in [4, 6, 4]:
            self.sprites_right['walking'].append(sprites_right[i])
        for i in [2, 4, 2]:
            self.sprites_left['walking'].append(sprites_left[size_x-i])

        self.sprites_right['jumping'] = []
        self.sprites_left['jumping'] = []
        self.sprites_right['jumping'].append(sprites_right[2])
        self.sprites_left['jumping'].append(sprites_left[4])

        self.sprites_right['crouching'] = []
        self.sprites_left['crouching'] = []
        self.sprites_right['crouching'].append(sprites_right[5])
        self.sprites_left['crouching'].append(sprites_left[3])

    def reset_frame(self):
        """

        """
        self.current_frame = 0
        self.ticks = 0

    def render(self, surface: pygame.Surface):
        if self.current_state == PlayerState.STANDING:
            if self.direction == PlayerState.RIGHT:
                frame = self.sprites_right[PlayerState.STANDING][self.current_frame]
            else:
                frame = self.sprites_left[PlayerState.STANDING][self.current_frame]

        elif self.current_state == PlayerState.WALKING:
            if self.direction == PlayerState.RIGHT:
                frame = self.sprites_right[PlayerState.WALKING][self.current_frame]
            else:
                frame = self.sprites_left[PlayerState.WALKING][self.current_frame]
            
        elif self.current_state == PlayerState.JUMPING:
            if self.direction == PlayerState.RIGHT:
                frame = self.sprites_right[PlayerState.JUMPING][self.current_frame]
            else:
                frame = self.sprites_left[PlayerState.JUMPING][self.current_frame]

        elif self.current_state == PlayerState.CROUCHING:
            if self.direction == PlayerState.RIGHT:
                frame = self.sprites_right[PlayerState.CROUCHING][self.current_frame]
            else:
                frame = self.sprites_left[PlayerState.CROUCHING][self.current_frame]

        surface.blit(frame, (self.pos_x, self.pos_y))

    def face_right(self):
        self.direction = PlayerState.RIGHT

    def face_left(self):
        self.direction = PlayerState.LEFT

    def gravity(self):
        self.pos_y += self.gravity_speed + self.current_jump

    def snap(self, collision, offset):

        # Get the dimensions of the player
        top = self.pos_y
        bottom = self.pos_y + constants.PLAYER_SIZE
        left = self.pos_x
        right = self.pos_x + constants.PLAYER_SIZE

        if collision == COLLISION_BOTTOM:
            self.pos_y -= bottom % constants.TILESIZE

        if collision == COLLISION_TOP:
            self.pos_y += constants.TILESIZE - (top % constants.TILESIZE)

        if collision == COLLISION_LEFT:
            self.pos_x += constants.TILESIZE - (left%constants.TILESIZE)

        if collision == COLLISION_RIGHT:
            self.pos_x -= right % constants.TILESIZE

    def collision_left(self, colliders, anchor_x, anchor_y):

        # Reset collisions
        collisions = []

        # Check if colliding with the map
        for collider in colliders:
            collisions += self.boundaries.get_left_collision(self.pos_x + anchor_x, self.pos_y + anchor_y, collider, collider.pos_x, collider.pos_y)
            
        return collisions

    def collision_right(self, colliders, anchor_x, anchor_y):

        # Reset collisions
        collisions = []

        # Check if colliding with the map
        for collider in colliders:
            collisions += self.boundaries.get_right_collision(self.pos_x + anchor_x, self.pos_y + anchor_y, collider, collider.pos_x, collider.pos_y)
            
        return collisions

    def collision_bottom(self, colliders, anchor_x, anchor_y):

        # Reset collisions
        collisions = []

        # Check if colliding with the map
        for collider in colliders:
            collisions += self.boundaries.get_bottom_collision(self.pos_x + anchor_x, self.pos_y + anchor_y, collider, collider.pos_x, collider.pos_y)
            
        return collisions

    def collision_top(self, colliders, anchor_x, anchor_y):

        # Reset collisions
        collisions = []

        # Check if colliding with the map
        for collider in colliders:
            collisions += self.boundaries.get_top_collision(self.pos_x + anchor_x, self.pos_y + anchor_y, collider, collider.pos_x, collider.pos_y)
            
        return collisions
        
    def walk(self, anchor_x, anchor_y, max_anchor_x, left = False, right = False):
        if self.current_state != PlayerState.JUMPING:
            # Set the state to walking
            self.current_state = PlayerState.WALKING

            # Update the animation frame
            self.ticks += 1
            if self.ticks > 60:
                self.current_frame = self.current_frame + 1 if self.current_frame < len(self.sprites_left[PlayerState.WALKING]) - 1 else 0 
                self.ticks = 0
        
        # Update the position
        if left:
            if self.pos_x <= constants.SCREEN_SIZE[0]/2 and anchor_x==0:
                self.pos_x -= self.player_speed

            elif self.pos_x >= constants.SCREEN_SIZE[0]/2 and anchor_x>=max_anchor_x:
                self.pos_x -= self.player_speed

            else:
                anchor_x -= self.player_speed
                if anchor_x < 0:
                    self.pos_x += anchor_x
                    anchor_x = 0
        if right:
            if self.pos_x >= constants.SCREEN_SIZE[0]/2 and anchor_x<max_anchor_x:
                anchor_x += self.player_speed
                if anchor_x > max_anchor_x:
                    self.pos_x += anchor_x - max_anchor_x
                    anchor_x = max_anchor_x
            else:
                self.pos_x += self.player_speed

        return anchor_x, anchor_y


    def stand(self):
        if self.current_state != PlayerState.JUMPING:
            self.reset_frame()
            self.current_state = PlayerState.STANDING

    def start_jump(self):
        if self.current_state != PlayerState.JUMPING and self.ground_state == PlayerState.GROUNDED:
            self.reset_frame()
            self.current_state = PlayerState.JUMPING
            self.current_jump = self.jump_speed

    def jump(self):
        self.current_jump += 0.01
        if self.current_jump >= 0:
            self.current_jump = 0
        
    def update(self, map:Map, anchor_x, anchor_y):

        # Jump
        if self.current_state == PlayerState.JUMPING:
            self.jump()
        
        # Apply gravity
        self.gravity()

        # By default, player is in air
        self.ground_state = PlayerState.AIR

        parsed_collisions = []
        col = self.collision_bottom(map.colliders.colliders, anchor_x, anchor_y)

        # Left here for debug
        self.col = col

        # Check collisions with map and snap positions
        for collision_type, offset, junk in col:

            # If touching the ground, set as GROUNDED
            if collision_type == COLLISION_BOTTOM:
                self.ground_state = PlayerState.GROUNDED
                
                if self.current_state == PlayerState.JUMPING:
                    self.reset_frame()
                    self.current_jump = 0
                    self.current_state = PlayerState.STANDING

            if collision_type not in parsed_collisions:
                self.snap(collision_type, offset)
                parsed_collisions.append(collision_type)

        parsed_collisions = []
        col = self.collision_top(map.colliders.colliders, anchor_x, anchor_y)

        # Left here for debug
        self.col += col

        # Check collisions with map and snap positions
        for collision_type, offset, junk in col:
            
            if collision_type == COLLISION_TOP:           
                if self.current_state == PlayerState.JUMPING:
                    self.reset_frame()
                    self.current_jump = 0
                    self.current_state = PlayerState.STANDING

            if collision_type not in parsed_collisions:
                self.snap(collision_type, offset)
                parsed_collisions.append(collision_type)

        parsed_collisions = []
        col = self.collision_right(map.colliders.colliders, anchor_x, anchor_y)

        # Left here for debug
        self.col += col

        # Check collisions with map and snap positions
        for collision_type, offset, junk in col:

            if collision_type not in parsed_collisions:
                self.snap(collision_type, offset)
                parsed_collisions.append(collision_type)

        parsed_collisions = []
        col = self.collision_left(map.colliders.colliders, anchor_x, anchor_y)
        self.col += col

        # Check collisions with map and snap positions
        for collision_type, offset, junk in col:

            if collision_type not in parsed_collisions:
                self.snap(collision_type, offset)
                parsed_collisions.append(collision_type)
