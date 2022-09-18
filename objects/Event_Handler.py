import abc
from abc import ABC, abstractmethod
import pygame
import pygame_gui
import numpy as np
from objects import World
from objects import GUI
from objects import Pendulum

class event_handler(ABC) :
    @abstractmethod
    def setGUI() :
        pass

    @abstractmethod
    def setWorld() :
        pass

    @abstractmethod
    def setState() :
        pass

    @abstractmethod
    def handleEvents() :
        pass

    @abstractmethod
    def _handleQuit() :
        pass

    @abstractmethod
    def _handleMouseButtonDown() :
        pass

    @abstractmethod
    def _handleMouseButtonUp() :
        pass

    @abstractmethod
    def _handleGUIEvents() :
        pass

class pensim_event_handler(event_handler) :
    def __init__(self, gui, world, state) :
        self._gui = gui
        self._world = world
        self._state = state

    def setGUI(self, gui) :
        self._gui = gui

    def setWorld(self, world) :
        self._world = world

    def setState(self, state) :
        self._state = state

    def handleEvents(self, events) :
        for event in events :
            if event.type == pygame.QUIT :
                self._handleQuit()
            if self._state.stopped and event.type == pygame.MOUSEBUTTONDOWN :
                self._handleMouseButtonDown(event)
            if event.type == pygame.MOUSEBUTTONUP :
                self._handleMouseButtonUp()
            if event.type == pygame_gui.UI_BUTTON_PRESSED :
                self._handleGUIEvents(event)
            self._gui.processEvents(event)

    def _handleQuit(self) :
        self._state.running = False

    def _handleMouseButtonDown(self, event) :
        mousex, mousey = event.pos
        pendula = self._world.getObjectStack()
        pendula = [x for x in pendula if issubclass(type(x), Pendulum.pendulum)]
        for pend in pendula :
            xpos, ypos = pend.getPos()
            radius = pend.getRadius()
            for i in range(pend.getN()) :
                dist = (xpos[i] - mousex)**2 + (ypos[i] - mousey)**2
                dist = np.sqrt(dist)
                if dist < radius[i] :
                    pend.setForcingState(True, i)
                    self._state.forcing = True

    def _handleMouseButtonUp(self) :
        pendula = self._world.getObjectStack()
        pendula = [x for x in pendula if issubclass(type(x), Pendulum.pendulum)]
        for pend in pendula :
            for i in range(pend.getN()) :
                pend.setForcingState(False, i)
        self._state.forcing = False

    def _handleGUIEvents(self, event) :
        if event.ui_element == self._gui.getStopButton() :
            self._state.stopped = not self._gui.toggleStopButton()
