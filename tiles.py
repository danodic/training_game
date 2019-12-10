import pygame

class Tileset:

    def __init__(self, filename:str, tilesize:int):
        # Store the tile size
        self.tilesize:int = tilesize

        # Initialize the sprite list
        self.sprites = []

        # Load the tiles
        self.__load_tileset(filename)

    def __load_tileset(self, filename:str):
        # Load the full image
        full_tileset = pygame.image.load(filename)

        # Get the tile count
        count_x = int(full_tileset.get_width()/self.tilesize)
        count_y = int(full_tileset.get_height()/self.tilesize)

        # Iterate over the tileset
        for x in range(0, count_x):
            for y in range(0, count_y):
                # Create the new tile and store it
                new_tile = pygame.Surface((self.tilesize, self.tilesize), pygame.SRCALPHA)
                new_tile.blit(full_tileset, (0,0), (x*self.tilesize, y*self.tilesize, self.tilesize, self.tilesize))
                self.sprites.append(new_tile)

    def get_tile(self, index):
        return self.sprites[index]
        