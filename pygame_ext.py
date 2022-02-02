from asyncio.constants import SENDFILE_FALLBACK_READBUFFER_SIZE
from multiprocessing import Event
from turtle import onclick
from cv2 import BORDER_REPLICATE
import pygame
from pygame.locals import *

class Events:
    def __init__(self) -> None:
        self.__events = []
    
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
        pygame.font.init()

        if resizable:
            self.screen = pygame.display.set_mode(size, RESIZABLE)

        self.left_clicks_down = Events()
        self.left_clicks_up = Events()
        self.right_clicks_down = Events()
        self.right_clicks_up = Events()
        self.other_events = Events()

        self.button_returns = Events()

        self.__buttons = []

    def set_background_color(self, bgcolor):
        self.bgcolor = bgcolor
    
    def set_tick_time(self, tick_time):
        self.tick_time = tick_time

    def __events_sorting(self):
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    ex = False
                    for b in self.__buttons:
                        if not b.disabled and not b.hidden:
                            if b.is_inside(e.pos):
                                r = b.click()
                                self.__button_returns.push_event([b,r])
                                ex = False

                    if not ex:
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

    def add_button(self, button):
        self.__buttons.append(button)

    def remove_button(self, button):
        self.__buttons.remove(button)

    def clear_buttons(self):
        self.__buttons = []

    def render_buttons(self, render_disabled=True):
        for b in self.__buttons:
            if not (b.disabled and not render_disabled):
                b.render(self.screen)


class Button:
    def __init__(self, *, size=(100,30), pos=(0,0), bgcolor=(255,255,255), border_color=(-1,-1,-1), border_width=1, border_radius, text="Button", text_color=(255,255,255), font_size=18, onclick=None, onclick_args=[], disabled=False, hidden=False) -> None:
        self.size = size
        self.pos = pos
        self.bgcolor = bgcolor

        if (-1,-1,-1) != border_color:
            self.border_color = border_color
        else:
            self.border_color = bgcolor

        self.border_width = border_width

        self.border_radius = border_radius
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.onclick = onclick
        self.onclick_args = onclick_args
        self.disabled = disabled
        self.need_to_be_enabled = False
        self.hidden = hidden

    def set_size(self, size):
        self.size = size
    def get_size(self):
        return self.size

    def set_pos(self, pos):
        self.pos = pos
    def get_pos(self):
        return self.pos

    def set_bgcolor(self, bgcolor):
        self.bgcolor= bgcolor
    def get_bgcolor(self):
        return self.bgcolor

    def set_border_color(self, border_color):
        self.border_color= border_color
    def get_border_color(self):
        return self.border_color
    
    def set_border_width(self, border_width):
        self.border_width = border_width
    def get_border_width(self):
        return self.border_width

    def set_border_radius(self, border_radius):
        self.border_radius = border_radius
    def get_border_radius(self):
        return self.border_radius

    def set_text(self, text):
        self.text = text
    def get_text(self):
        return self.text

    def set_text_color(self, text_color):
        self.text_color = text_color
    def get_text_color(self):
        return self.text_color

    def set_font_size(self, font_size):
        self.font_size = font_size
    def get_font_size(self):
        return self.font_size

    def set_onclick(self, onclick):
        self.onclick = onclick
    def get_onclick(self):
        return self.onclick

    def set_onclick_args(self, onclick_args):
        self.onclick_args = onclick_args
    def get_onclick_args(self):
        return self.onclick_args

    def is_inside(self, pos):
        x,y = self.pos
        xp,yp = pos
        w,h = self.size

        if xp < x or xp > x+w:
            return False
        if yp < y or yp > y+h:
            return False
        return True

    def disable(self):
        self.disabled = True
    def enable(self):
        self.disabled = False
        self.need_to_be_enabled = False

    def hide(self):
        self.hidden = True
    def show(self):
        self.hidden = False

    def render(self, screen):
        font = pygame.font.SysFont("Comic Sans MS", self.font_size)
        pygame.draw.rect(screen, self.bgcolor, pygame.Rect(self.pos, self.size),0, self.border_radius)
        pygame.draw.rect(screen, self.bgcolor, pygame.Rect(self.pos, self.size),self.radius_width, self.border_radius)

        text_surface = font.render(self.text, False, self.text_color)

        r = text_surface.get_rect()

        dx = (self.size[0]-r.width)//2
        dy = (self.size[1]-r.height)//2
        screen.blit(text_surface, (self.pos[0]+dx, self.pos[1]+dy))
        
    def click(self):
        if self.onclick_args == []:
            return self.onclick()
        else:
            return self.onclick(self.onclick_args)
