import abc
from abc import ABC, abstractmethod
import numpy as np
import pygame
from objects import Physics
from objects import Drawable

class pendulum(Drawable.drawable) :
    def __init__(self, phys, world) :
        super().__init__(world)
        self._gravity = phys.gravity
        self._friction = phys.friction
    
    @abstractmethod
    def eom(self) :
        pass

class pendulum1M(pendulum) :
    def __init__(self, length, mass, theta, omega, phys, world) :
        super().__init__(phys, world)
        self._length = [length]
        self._mass = [mass]
        self._theta = [theta]
        self._omega = [omega]
        self._x = [self._length[0] * np.sin(self._theta[0])]
        self._y = [-self._length[0] * np.cos(self._theta[0])]
        self._alpha = [None]*1
        self.eom()

    def eom(self) :
        self._alpha[0] = self._gravity*np.sin(self._theta[0])/self._length[0] - self._friction*self._omega[0]

    def draw(self) :
        # pass to function
        screenw = self._world.getEffWidth()
        screenh = self._world.getEffHeight()
        tmargin, rmargin, bmargin, lmargin = self._world.getMargin()
        x = self._x[0] / self._world.getScale() + lmargin + screenw/2
        y = -self._y[0] / self._world.getScale() + tmargin + screenh/10
        print(screenw)

        screen = self._world.getScreen()
        bgcolor = self._world.getBackgroundColor()
        screen.fill(bgcolor)
        self._massrect = pygame.draw.circle(screen, (0,0,255), (x, y), 20, 5)
        pygame.display.update()

class pendulum1MEuler(pendulum1M) :
    def update(self, dt) :
        self._theta[0] = self._theta[0] + self._omega[0]*dt + 0.5*self._alpha[0]*dt*dt
        self._omega[0] = self._omega[0] + self._alpha[0]*dt
        self._x[0] = self._length[0] * np.sin(self._theta[0])
        self._y[0] = -self._length[0] * np.cos(self._theta[0])
        self.eom()
