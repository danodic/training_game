"""
This module contains the classes used to manage the maps in the game. Each map
is compound by 3 layers: background, foreground and a collision layer. Each one
of the layers can use a different tileset, that has to be imported from the
tiles module.
"""
import pygame
import csv
import math

from typing import Tuple, List

from pygame import Surface
from tiles import Tileset
from collisions import BoundingBox
from constants import TILESIZE, SCREEN_SIZE

class MapLayer:
    """
    The map layer contains the actual information of a map, inclusing the tile
    coordinates and collision boundaries in case of a collision layer.
    This is used also to render the map in the screen.
    """

    def __init__(self, filename:str, tileset:Tileset, is_collidable:bool = False):
        # Initialize values
        self.colliders: List[BoundingBox] = []
        
        # Store values
        self.filename: str = filename
        self.is_collidable: bool = is_collidable
        self.tileset: Tileset = tileset

        # Parse the tiles
        self.tiles = self.__parse_tiles(filename)

        # Parse colliders if needed
        if is_collidable:
            self.colliders = self.__parse_colliders(self.tiles)
    
    def __parse_tiles(self, filename: str):
        """
        Load the map as a CSV file.
        """
        with open(filename, 'r') as file:
            tiles = list(csv.reader(file))
        return tiles

    def __parse_colliders(self, tiles):
        """
        Load the colliders in a CSV file.
        """
        colliders = []
        # Iterate over rows and columns 
        for row_pos, row in enumerate(self.tiles):
            for column_pos, column in enumerate(row):
                # Check if empty, if so ignore it
                if not column:
                    continue

                # Create the bounding box
                bbox = BoundingBox(TILESIZE, TILESIZE)
                bbox.pos_x = column_pos * TILESIZE
                bbox.pos_y = row_pos * TILESIZE

                # Add to the list
                colliders.append(bbox)

        return colliders

    def render(self, anchor_x:int, anchor_y:int, screen_size:Tuple[int], surface:Surface):
        """
        Will render the map on the surface provided.
        """
        # Define the render frame for the X axis
        start_x = math.floor(anchor_x / TILESIZE)
        end_x = start_x + math.ceil(SCREEN_SIZE[0] / TILESIZE) + 1

        # Define the render frame for the Y axis
        end_y = len(self.tiles) - math.floor(anchor_y / TILESIZE)
        start_y = end_y - math.floor(SCREEN_SIZE[1] / TILESIZE)
        start_y = 0 if start_y < 0 else start_y

        # Define the anchor offset for the tiles
        anchor_x = - int(anchor_x % TILESIZE)

        # Iterate over rows and columns 
        for row_pos, row in enumerate(self.tiles[start_y:end_y]):
            for column_pos, column in enumerate(row[start_x:end_x]):

                # Check if empty, if so ignore it
                if not column:
                    continue

                # Get the positions based on tilesize
                pos_x = anchor_x + (column_pos * self.tileset.tilesize)
                pos_y = anchor_y + (row_pos * self.tileset.tilesize)
                # Blit on the screen
                surface.blit(self.tileset.get_tile(int(column)), (pos_x, pos_y))

                

class Map:
    """
    Will store the full information of a map.
    """
    def __init__(self):
        # Initialize layers
        self.foreground: MapLayer = None
        self.background: MapLayer = None
        self.colliders: MapLayer = None

    def load_background(self, filename:str, tileset:Tileset):
        """
        Will load a background tileset from a CSV file.
        """
        self.background = MapLayer(filename, tileset)

    def load_foreground(self, filename:str, tileset:Tileset):
        """
        Will load a foreground tileset from a CSV file.
        """
        self.foreground = MapLayer(filename, tileset)

    def load_colliders(self, filename:str, tileset:Tileset):
        """
        Will load the collision layer from a CSV file.
        """
        self.colliders = MapLayer(filename, tileset, True)