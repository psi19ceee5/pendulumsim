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

        self._stop_button_state = False
        effwidth = world.getEffWidth()
        effheight = world.getEffHeight()
        tmargin, rmargin, bmargin, lmargin = world.getMargin()
        sbutton_w = int(0.15*effwidth)
        sbutton_h = int(0.1*effheight)
        sbutton_x = lmargin + effwidth - sbutton_w
        sbutton_y = tmargin + effheight - 2*int(1.2*sbutton_h)
        self._sbutton_rect = pygame.Rect((sbutton_x, sbutton_y), (sbutton_w, sbutton_h))
        self._setButton()

    def _showStopButton(self) :
        self._stop_button_state = True
        self._setButton()

    def _showReleaseButton(self) :
        self._stop_button_state = False
        self._setButton()

    def _setButton(self) :
        self._guimanager.clear_and_reset()
        if self._stop_button_state :
            self._stop_button = pygame_gui.elements.UIButton(relative_rect=self._sbutton_rect,
                                                             text='Stop',
                                                             manager=self._guimanager)
        else :
            self._stop_button = pygame_gui.elements.UIButton(relative_rect=self._sbutton_rect,
                                                             text='Release',
                                                             manager=self._guimanager)
        
    def getStopButton(self) :
        return self._stop_button

    def toggleStopButton(self) :
        if self._stop_button_state :
            self._showReleaseButton()
        else :
            self._showStopButton()

        return self._stop_button_state
