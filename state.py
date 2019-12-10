"""
This module handles the state of the game. Things like the Game or the input
state.
"""

import pygame

class GameController:
    """
    This class stores the game state.
    """
    def __init__(self):
        self.done = False

class InputController:
    def __init__(self):
        self.left = False
        self.up = False
        self.right = False
        self.down = False
        self.quit = False
        self.jump = False

    def update(self):

        # Reset push-once buttons
        self.jump = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left = True

                if event.key == pygame.K_RIGHT:
                    self.right = True

                if event.key == pygame.K_UP:
                    self.up = True

                if event.key == pygame.K_DOWN:
                    self.down = True

                if event.type == pygame.KEYDOWN:
                    self.jump = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left = False

                if event.key == pygame.K_RIGHT:
                    self.right = False

                if event.key == pygame.K_UP:
                    self.up = False

                if event.key == pygame.K_DOWN:
                    self.down = False

            if event.type == pygame.KEYDOWN:
                self.jump = event.key == pygame.K_SPACE