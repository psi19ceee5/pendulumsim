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
    world.setRelMargin(0.1, 0.1, 0.1, 0.1)
    world.initPyGame()
    
    phys = Physics.physics()
    pend = Pendulum.pendulum1MEuler([0.2], [1], [np.pi/4.], [0], phys, world)

    world.appendObject(pend)

    clock = pygame.time.Clock()

    t0 = 0
    t1 = 0
    fps = 45
    running = True
    while running:
        clock.tick(fps)
        tcyc = int(1000./fps)
        # num iteration in small steps (delay main loop)
        t0 = pygame.time.get_ticks()
        t1 = pygame.time.get_ticks()
        dt = 0
        while t1 - t0 < tcyc :
            t1 = pygame.time.get_ticks()
            world.update(dt/1000.)
            pygame.time.delay(1)
            dt = pygame.time.get_ticks() - t1
        
        world.draw()
        
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                running = False
