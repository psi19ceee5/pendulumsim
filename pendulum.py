#!/usr/bin/env python3

import abc
from abc import ABC, abstractmethod
import numpy as np
import pygame

screenw = 600
screenh = 600

class drawable(ABC) :
    @abstractmethod
    def draw(self) :
        pass

    @abstractmethod
    def update(self) :
        pass

class pendulum(drawable) :
    @abstractmethod
    def eom(self) :
        pass

class pendulum1M(pendulum) :
    def __init__(self, length, mass, theta, omega) :
        self._length = length
        self._mass = mass
        self._theta = theta
        self._omega = omega
        self._alpha = self.eom()
        self._x = self._length * np.sin(self._theta)
        self._y = -self._length * np.cos(self._theta)

    def eom(self) :
        # beta = 0.01, g = 9.81 (world properties)
        return -9.81*np.sin(self._theta)/self._length - 0.1*self._omega

    def draw(self) :
        # pass to function
        x = self._x * (0.5*screenw/self._length) + screenw/2
        y = -self._y * (0.5*screenh/self._length) + screenh/10
        # pygame test
        screen.fill((255,255,255))
        self._massrect = pygame.draw.circle(screen, (0,0,255), (x, y), 20, 5) #(r, g, b) is color, (x, y) is center, (R, w) is radius and width.
        pygame.display.update()        

class pendulum1MEuler(pendulum1M) :
    def update(self, dt) :
        self._theta = self._theta + self._omega*dt + 0.5*self._alpha*dt*dt
        self._omega = self._omega + self._alpha*dt
        self._alpha = self.eom()
        self._x = self._length * np.sin(self._theta)
        self._y = -self._length * np.cos(self._theta)         

    def print(self) :
        print(self._theta, self._omega, self._alpha)        

if __name__ == "__main__" :
    # pend = pendulum1MEuler(1, 1, np.pi/4, 0)
    
    # pygame test
    pygame.init()
    screen = pygame.display.set_mode((screenw, screenh))

    pygame.display.set_caption("Pendulum Simulation")
    screen.fill((255,255,255))

    pend = pendulum1MEuler(1, 1, np.pi/4, 0)

    running = True
    while running:
        pend.draw()
        pend.update(0.001)
        
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False
