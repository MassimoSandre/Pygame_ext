from multiprocessing import Event
import pygame
from pygame.locals import *

class Events:
    def __init__(self) -> None:
        self.events = []
    
    def push_event(self, e):
        self.events.append(e)

    def get(self):
        events = self.events
        self.events = []
        return events


class Pygame_ext:
    def __init__(self,*, size=(620,540), bgcolor=(0,0,0), tick_time=60, resizable=False) -> None:
        self.size = self.width, self.height = size
        self.clock = pygame.time.Clock()
        self.tick_time = tick_time
        self.bgcolor = bgcolor

        if resizable:
            self.screen = pygame.display.set_mode(size, RESIZABLE)

        self.__left_clicks_down = Events()
        self.__left_clicks_up = Events()
        self.__right_clicks_down = Events()
        self.__right_clicks_up = Events()
        self.__other_events = Events()

    def __events_sorting(self):
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.__left_clicks_down.push_event(e)
                elif e.button == 3:
                    self.__right_clicks_down.push_event(e)
                else:
                    self.__other_events.push_event(e)
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    self.__left_clicks_up.push_event(e)
                elif e.button == 3:
                    self.__right_clicks_up.push_event(e)
                else:
                    self.__other_events.push_event(e)


    def loop(self):
        pygame.display.update()
        self.clock.tick(self.tick_time)
        self.screen.fill(self.bgcolor)


class Button:
    def __init__(self, *, size=(100,30), bgcolor=(255,255,255), text="Button", text_color=(255,255,255), font_size=18, onclick=None, onclick_args=[], disabled=False) -> None:
        events = Events()
        self.bgcolor = bgcolor
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.onclick = onclick
        self.onclick_args = onclick_args
        self.disabled = disabled

    def disable(self):
        self.disabled = True
    def enable(self):
        self.disabled = False