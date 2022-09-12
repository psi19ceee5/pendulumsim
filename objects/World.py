import pygame
import pygame_gui
from objects import Drawable

class world(Drawable.drawable) :
    def __init__(self) :
        self._object_stack = []
        self._background_color = (255, 255, 255)
        self._width = 800
        self._height = 600
        self._tmargin = 0
        self._rmargin = 0
        self._bmargin = 0
        self._lmargin = 0
        self._effwidth = self._width
        self._setEffWidth()
        self._effheight = self._height
        self._setEffHeight()
        self._aspectratio = self._setAspectRatio()
        self._effapectratio = self._setEffAspectRatio()
        self._scale = 0.002 # meter per pixel
        self._screen = None
        self._guimanager = None
        self._stop_button = None
        self._release_button = None

    def initPyGame(self) :
        pygame.init()
        self._screen = pygame.display.set_mode((self._width, self._height))
        pygame.display.set_caption("Pendulum Simulation")

    def initGUI(self) :
        self._guimanager = pygame_gui.UIManager((self._width, self._height))
        sbutton_w = int(0.15*self._effwidth)
        sbutton_h = int(0.1*self._effheight)
        sbutton_x = self._lmargin + self._effwidth - sbutton_w
        sbutton_y = self._height - self._bmargin - 2*int(1.2*sbutton_h)
        sbutton_rect = pygame.Rect((sbutton_x, sbutton_y), (sbutton_w, sbutton_h))
        self._stop_button = pygame_gui.elements.UIButton(relative_rect=sbutton_rect,
                                                         text='Stop',
                                                         manager=self._guimanager)
        rbutton_w = sbutton_w
        rbutton_h = sbutton_h
        rbutton_x = sbutton_x
        rbutton_y = self._height - self._bmargin - 1*int(1.2*sbutton_h)
        rbutton_rect = pygame.Rect((rbutton_x, rbutton_y), (rbutton_w, rbutton_h))
        self._release_button = pygame_gui.elements.UIButton(relative_rect=rbutton_rect,
                                                            text='Release',
                                                            manager=self._guimanager)

        
    def appendObject(self, drawobject) :
        assert issubclass(type(drawobject), Drawable.drawable)
        self._object_stack.append(drawobject)

    def clearObjectStack(self) :
        for obj in self._object_stack :
            del obj
        self._object_stack = []

    def draw(self) :
        for obj in self._object_stack :
            obj.draw()
        self._guimanager.draw_ui(self._screen)
        pygame.display.update()


    def update(self, dt) :
        for obj in self._object_stack :
            obj.update(dt)

    def updateGUI(self, time_delta) :
        self._guimanager.update(time_delta)

    def setBackgroundColor(self, color) :
        self._background_color = color

    def setScale(self, scale) :
        self._scale = scale

    def setWidth(self, width) :
        self._width = width
        self._setEffWidth()
        pygame_gui.UIManager((self._width, self._height))

    def setHeight(self, height) :
        self._height = height
        self._setEffHeight()
        pygame_gui.UIManager((self._width, self._height))

    def setWorldWidth(self, width) :
        self._width = width/self._scale
        self._setEffWidth()
        pygame_gui.UIManager((self._width, self._height))

    def setWorldHeight(self, height) :
        self._height = height/self._scale
        self._setEffHeight()
        pygame_gui.UIManager((self._width, self._height))

    def setMargin(self, tmargin, rmargin, bmargin, lmargin) :
        self._tmargin = tmargin
        self._rmargin = rmargin
        self._bmargin = bmargin
        self._lmargin = lmargin
        self._setEffWidth()
        self._setEffHeight()

    def setRelMargin(self, tmargin, rmargin, bmargin, lmargin) :
        self._tmargin = tmargin*self._height
        self._rmargin = rmargin*self._width
        self._bmargin = bmargin*self._height
        self._lmargin = lmargin*self._width
        self._setEffWidth()
        self._setEffHeight()

    def _setEffWidth(self) :
        self._effwidth = self._width - self._rmargin - self._lmargin

    def _setEffHeight(self) :
        self._effheight = self._height - self._tmargin - self._bmargin 

    def _setAspectRatio(self) :
        return self._width/self._height

    def _setEffAspectRatio(self) :
        return self._effwidth/self._effheight

    def getGUIManager(self) :
        return self._guimanager

    def getBackgroundColor(self) :
        return self._background_color

    def getScreen(self) :
        return self._screen

    def getScale(self) :
        return self._scale

    def getWidth(self) :
        return self._width

    def getHeight(self) :
        return self._height

    def getWorldWidth(self) :
        return self._width*self._scale

    def getWorldHeight(self) :
        return self._height*self._scale

    def getMargin(self) :
        return self._tmargin, self._rmargin, self._bmargin, self._lmargin

    def getRelMargin(self) :
        return tmargin/self._height, rmargin/self._width, bmargin/self._height, lmargin/self._width

    def getEffWidth(self) :
        return self._effwidth

    def getEffHeight(self) :
        return self._effheight

    def getAspectRatio(self) :
        return self._aspectratio

    def getEffAspectRatio(self) :
        return self._effaspectratio

    def getStopButton(self) :
        return self._stop_button

    def getReleaseButton(self) :
        return self._release_button
