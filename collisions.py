"""
The collisions package has code related to detecting collisions in the game
engine.
"""

# Some constants / Define which kind of collision is happening
COLLISION_TOP = 1
COLLISION_BOTTOM = 2
COLLISION_LEFT = 3
COLLISION_RIGHT = 4

class BoundingBox:
    """
    Represents a bounding box and has a method to validate collisions. It is not
    position-aware, but we inject some position variables when parsing the map
    colliders in order to simplify the process of calculating collisions with
    the map itself.
    """
    
    def __init__(self, width:int, heigth:int):
        # Copy values
        self.width = width
        self.heigth = heigth

    def get_top_collision(self, pos_x, pos_y, other, other_pos_x, other_pos_y):
        collisions = []

        # Get the coordinates to test
        # Get the boundaries of self
        self_left = pos_x
        self_right = pos_x + self.width
        self_top = pos_y
        self_bottom = pos_y + self.heigth

        # Get the boundaries of other
        other_left = other_pos_x
        other_right = other_pos_x + other.width
        other_top = other_pos_y
        other_bottom = other_pos_y + other.heigth

        # Check if colliding at the bottom
        if self_top < other_bottom and self_bottom > other_bottom and (self_left < other_right and self_right > other_left):
            collisions.append((COLLISION_TOP, other_bottom - self_top, (other_left, other_top, 64, 64)))
            pass

        return collisions

    def get_bottom_collision(self, pos_x, pos_y, other, other_pos_x, other_pos_y):

        collisions = []

        # Get the boundaries of self
        self_left = pos_x
        self_right = pos_x + self.width
        self_top = pos_y
        self_bottom = pos_y + self.heigth

        # Get the boundaries of other
        other_left = other_pos_x
        other_right = other_pos_x + other.width
        other_top = other_pos_y
        other_bottom = other_pos_y + other.heigth

        # Check if colliding at the bottom
        if self_bottom > other_top and self_top < other_top and (self_left < other_right and self_right > other_left):
            collisions.append((COLLISION_BOTTOM, other_top - self_bottom, (other_left, other_top, 64, 64)))

        return collisions

    def get_left_collision(self, pos_x:int, pos_y:int, other, other_pos_x:int, other_pos_y:int):
        
        collisions = []

        # Get the coordinates to test
        # Get the boundaries of self
        self_left = pos_x
        self_right = pos_x + self.width
        self_top = pos_y
        self_bottom = pos_y + self.heigth

        # Get the boundaries of other
        other_left = other_pos_x
        other_right = other_pos_x + other.width
        other_top = other_pos_y
        other_bottom = other_pos_y + other.heigth

        # Check if colliding at the bottom
        if self_left < other_right and self_right > other_right and (self_top < other_bottom and self_bottom > other_top):
            collisions.append((COLLISION_LEFT, other_left - other_top, (other_left, other_top, 64, 64)))

        return collisions

    def get_right_collision(self, pos_x:int, pos_y:int, other, other_pos_x:int, other_pos_y:int):
        
        collisions = []

        # Get the coordinates to test
        # Get the boundaries of self
        self_left = pos_x
        self_right = pos_x + self.width
        self_top = pos_y
        self_bottom = pos_y + self.heigth

        # Get the boundaries of other
        other_left = other_pos_x
        other_right = other_pos_x + other.width
        other_top = other_pos_y
        other_bottom = other_pos_y + other.heigth

        # Check if colliding at the bottom
        if self_right > other_left and self_left < other_left and (self_top < other_bottom and self_bottom > other_top):
            collisions.append((COLLISION_RIGHT, other_left - other_top, (other_left, other_top, 64, 64)))

        return collisions
