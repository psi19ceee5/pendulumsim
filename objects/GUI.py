import pygame
import pygame_gui
from abc import abstractmethod
from objects import Drawable
from objects import World


class gui(Drawable.drawable) :
    @abstractmethod
    def __init__(self, world) :
        self._width = world.getWidth()
        self._height = world.getHeight()
        self._screen = world.getScreen()
        self._guimanager = pygame_gui.UIManager((self._width, self._height))

    def processEvents(self, event) :
        self._guimanager.process_events(event)

    def update(self, time_delta) :
        self._guimanager.update(time_delta)

    def draw(self) :
        self._guimanager.draw_ui(self._screen)
        pygame.display.update()
        

class pensimgui(gui) :
    def __init__(self, world) :
        super().__init__(world)

        self.showReleaseButton()

        effwidth = world.getEffWidth()
        effheight = world.getEffHeight()
        tmargin, rmargin, bmargin, lmargin = world.getMargin()
        sbutton_w = int(0.15*effwidth)
        sbutton_h = int(0.1*effheight)
        sbutton_x = lmargin + effwidth - sbutton_w
        sbutton_y = tmargin + effheight - 2*int(1.2*sbutton_h)
        sbutton_rect = pygame.Rect((sbutton_x, sbutton_y), (sbutton_w, sbutton_h))
        self._stop_button = pygame_gui.elements.UIButton(relative_rect=sbutton_rect,
                                                         text='Stop',
                                                         manager=self._guimanager)
        rbutton_w = sbutton_w
        rbutton_h = sbutton_h
        rbutton_x = sbutton_x
        rbutton_y = tmargin + effheight - 1*int(1.2*sbutton_h)
        rbutton_rect = pygame.Rect((rbutton_x, rbutton_y), (rbutton_w, rbutton_h))
        self._release_button = pygame_gui.elements.UIButton(relative_rect=rbutton_rect,
                                                            text='Release',
                                                            manager=self._guimanager)

    def getStopButton(self) :
        return self._stop_button


    def getReleaseButton(self) :
        return self._release_button

    def showStopButton(self) :
        self._show_stop_button = True
        self._show_release_button = False

    def showReleaseButton(self) :
        self._show_stop_button = False
        self._show_release_button = True
