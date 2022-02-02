import pygame
from pygame.locals import *

class Pygame_ext:
    def __init__(self,*, size=(620,540), bgcolor=(0,0,0), tick_time=60, resizable=False) -> None:
        self.size = self.width, self.height = size
        self.clock = pygame.time.Clock()
        self.tick_time = tick_time
        self.bgcolor = bgcolor

        if resizable:
            self.screen = pygame.display.set_mode(size, RESIZABLE)

    def loop(self):
        pygame.display.update()
        self.clock.tick(self.tick_time)
        self.screen.fill(self.bgcolor)