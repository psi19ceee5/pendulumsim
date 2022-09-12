#!/usr/bin/env python3

import abc
from abc import ABC, abstractmethod
import numpy as np
import pygame
import pygame_gui
from objects import World
from objects import Physics
from objects import Drawable
from objects import Pendulum


if __name__ == "__main__" :

    world = World.world()
    world.setRelMargin(0.1, 0.1, 0.1, 0.1)
    world.initPyGame()
    world.initGUI()
    
    phys = Physics.physics(friction=0.01)
    pend = Pendulum.pendulum2M(length=[0.4, 0.4],               
                                    mass=[1, 1],
                                    theta=[np.pi/2., 3*np.pi/4.],
                                    omega=[0, 0],
                                    phys=phys,
                                    world=world)

    world.appendObject(pend)

    clock = pygame.time.Clock()

    t0 = 0
    t1 = 0
    fps = 45
    running = True
    moving = True
    while running:
        time_delta = clock.tick(fps)

        if moving :
            tcyc = int(1000./fps)
            t0 = pygame.time.get_ticks()
            t1 = pygame.time.get_ticks()
            dt = 0
            while t1 - t0 < tcyc :
                t1 = pygame.time.get_ticks()
                world.update(dt/1000.)
                pygame.time.delay(1)
                dt = pygame.time.get_ticks() - t1
        
        ev = pygame.event.get()

        for event in ev :
            if event.type == pygame.QUIT :
                running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED :
                if event.ui_element == world.getStopButton() :
                    moving = False
                if event.ui_element == world.getReleaseButton() :
                    moving = True

            world.getGUIManager().process_events(event)

        world.updateGUI(time_delta)
        world.draw()

