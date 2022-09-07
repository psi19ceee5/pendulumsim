#!/usr/bin/env python3

import abc
from abc import ABC, abstractmethod
import numpy as np
import pygame
from objects import World
from objects import Physics
from objects import Drawable
from objects import Pendulum


if __name__ == "__main__" :
    # pend = pendulum1MEuler(1, 1, np.pi/4, 0)

    world = World.world()
    world.setRelMargin(0.2, 0.3, 0.1, 0.4)
    world.initPyGame()
    
    phys = Physics.physics()
    pend = Pendulum.pendulum1MEuler(1, 1, np.pi/4, 0, phys, world)

    world.appendObject(pend)

    running = True
    while running:
        world.draw()
        world.update(0.001)
        
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False
