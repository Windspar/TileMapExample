import os
import pygame

class Engine:
    @staticmethod
    def center_screen():
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    @staticmethod
    def screen_position(x, y):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '{}, {}'.format(x, y)

    def __init__(self, caption, width, height, flags=0, fps=60, center=False):
        if center:
            Engine.center_screen()

        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.running = False
        self.delta = 0
        self.fps = fps

    def idle(self):
        self.delta = self.clock.tick(self.fps)

    def quit(self):
        self.running = False
