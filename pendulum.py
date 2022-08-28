import abc
from abc import ABC, abstractmethod
import numpy as np
import pygame

class pendulum(ABC) :
    @abstractmethod
    def __init__(self) :
        pass

    @abstractmethod
    def Draw(self) :
        pass

    @abstractmethod
    def Update(self) :
        pass

class pendulum1M(pendulum) :
    def __init__(self, length, mass, theta, omega) :
        self._length = length
        self._mass = mass
        self._theta = theta
        self._omega = omega
        self._alpha = self.eom()
        self._x = self._length * np.sin(self._theta)
        self._y = - self._length * np.cos(self._theta) 

    def eom(self) :
        return -9.81*np.sin(self._theta)/self._length

    def Draw(self) :
        # not implemented yet #
        print("Drawing is not implemented yet.")

class pendulum1MEuler(pendulum1M) :
    def Update(self, dt) :
        self._theta = self._theta + self._omega*dt + 0.5*self._alpha*dt*dt
        self._omega = self._omega + self._alpha*dt
        self._alpha = self.eom()
        

    def Print(self) :
        print(self._theta, self._omega, self._alpha)
        

if __name__ == "__main__" :
    pend = pendulum1MEuler(1, 1, np.pi/4, 0)

    for t in range(10) :
        pend.Print()
        pend.Update(0.1)
    
    # pygame test
    pygame.init()
    screen = pygame.display.set_mode((600, 400)) #x and y are height and width

    pygame.display.set_caption("Pendulum Simulation")
    screen.fill((255,255,255))
    pygame.draw.circle(screen, (0,0,255), (0, 0), 20, 5) #(r, g, b) is color, (x, y) is center, (R, w) is radius and width.
    pygame.display.update()

    running = True
    while running:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False
