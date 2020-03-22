import pygame
import os

class Scene:
    live = {}

    # Manager Interface
    def __init__(self, manager, keep=False, name=None):
        self.manager = manager
        if keep:
            if name is None:
                name = self.__class__.__name__

            Scenes.live[name] = scene

    def scene_draw(self, surface):
        self.on_draw(surface)

    def scene_drop(self):
        self.on_drop()

    def scene_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_quit()
            else:
                self.on_event(event)

    def scene_focus(self, *args, **kwargs):
        self.on_focus(*args, **kwargs)

    def scene_new(self,*args, **kwargs):
        self.on_new(*args, **kwargs)

    def scene_update(self, delta):
        self.on_update(delta)

    def _flip(self, scene):
        if isinstance(scene, Scene):
            return scene
        else:
            return Scene.live[scene]

    def flip(self, scene, *args, **kwargs):
        self.manager.flip(self._flip(scene), *args, **kwargs)

    def flip_new(self, scene, *args, **kwargs):
        self.manager.flip_new(self._flip(scene), *args, **kwargs)

    def on_quit(self):
        self.manager.quit()

    # Scene Interface
    def on_draw(self, surface): pass
    def on_drop(self): pass
    def on_event(self, event): pass
    def on_focus(self): pass
    def on_new(self): pass
    def on_update(self, delta): pass

class Manager:
    def __init__(self, caption, width, height, center=True, flags=0):
        if center is True:
            os.environ['SDL_VIDEO_CENTERED'] = '1'
        elif center:
            os.environ['SDL_VIDEO_WINDOW_POS'] = '{}, {}'.format(*center)

        # Basic pygame setup
        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.running = False
        self.delta = 0
        self.fps = 60

        # Scene handling
        self._scene = Scene(self)
        self.scenes = {}

        self.extension = []

    def flip(self, scene, *args, **kwargs):
        self._scene.scene_drop()
        self._scene = scene
        self._scene.scene_focus(*args, **kwargs)

    def flip_new(self, scene, *args, **kwargs):
        self._scene.scene_drop()
        self._scene = scene
        self._scene.scene_new(*args, **kwargs)

    def mainloop(self):
        self.running = True
        while self.running:
            self._scene.scene_event()
            self._scene.scene_update(self.delta)
            self._scene.scene_draw(self.surface)
            for extension in self.extension:
                extension(self)

            pygame.display.flip()
            self.delta = self.clock.tick(self.fps)

    def quit(self):
        self.running = False
