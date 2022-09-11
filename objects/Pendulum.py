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
        self._mountpoint_width = 0.1*world.getEffWidth()
        self._mountpoint_height = 0.05*world.getEffHeight()
    
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
        self._mass_radius = []
        for m in self._mass :
            self._mass_radius.append(20*m**(1./3.))

    def eom(self) :
        self._alpha[0] = self._gravity*np.sin(self._theta[0])/self._length[0] - self._friction*self._omega[0]

    def draw(self) :
        screenw = self._world.getEffWidth()
        screenh = self._world.getEffHeight()
        tmargin, rmargin, bmargin, lmargin = self._world.getMargin()

        screen = self._world.getScreen()
        bgcolor = self._world.getBackgroundColor()
        screen.fill(bgcolor)

        # mass circle
        x = self._x[0] / self._world.getScale() + lmargin + screenw/2
        y = -self._y[0] / self._world.getScale() + tmargin + screenh/10
        pygame.draw.circle(screen,
                           (0,0,255),
                           (x, y),
                           int(self._mass_radius[0]),
                           int(0.25*self._mass_radius[0]))

        # suspension
        sus_x1 = lmargin + screenw/2.
        sus_y1 = tmargin + self._mountpoint_height
        sus_x2 = x - int(self._mass_radius*np.sin(self._theta))
        sus_y2 = y - int(self._mass_radius*np.cos(self._theta))
        pygame.draw.line(screen,
                         (0, 0, 0),
                         (sus_x1, sus_y1),
                         (sus_x2, sus_y2),
                         width=3)

        # mount point
        rectl = lmargin + screenw/2. - self._mountpoint_width/2.
        rectt = tmargin
        pygame.draw.rect(screen,
                         (157, 78, 40),
                         pygame.Rect((rectl, rectt),
                              (self._mountpoint_width,
                               self._mountpoint_height)))
        
        pygame.display.update()

class pendulum1MEuler(pendulum1M) :
    def update(self, dt) :
        self._theta[0] = self._theta[0] + self._omega[0]*dt + 0.5*self._alpha[0]*dt*dt
        self._omega[0] = self._omega[0] + self._alpha[0]*dt
        self._x[0] = self._length[0] * np.sin(self._theta[0])
        self._y[0] = -self._length[0] * np.cos(self._theta[0])
        self.eom()
