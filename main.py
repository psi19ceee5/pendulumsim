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
from objects import GUI


if __name__ == "__main__" :

    world = World.world()
    world.setRelMargin(0.1, 0.1, 0.1, 0.1)
    world.initPyGame()
    gui = GUI.pensimgui(world)
    
    phys = Physics.physics(friction=0.00)
    pend = Pendulum.pendulum2M(length=[0.4, 0.4],               
                                    mass=[1, 1],
                                    theta=[0, 0],
                                    omega=[0, 0],
                                    phys=phys,
                                    world=world)

    method = Pendulum.rk4(pend)
    pend.setNumMethod(method)

    world.appendObject(pend)

    clock = pygame.time.Clock()

    t0, t1 = 0, 0
    fps = 45
    num_time_interval = 1 # ms
    running = True
    stopped = True
    forcing = False
    while running:
        time_delta = clock.tick(fps)

        if not stopped :
            tcyc = int(1000./fps)
            t0 = pygame.time.get_ticks()
            t1 = pygame.time.get_ticks()
            dt = 0
            while t1 - t0 < tcyc :
                t1 = pygame.time.get_ticks()
                world.update(dt/1000.)
                pygame.time.delay(num_time_interval)
                dt = pygame.time.get_ticks() - t1
        
        if forcing :
            mousex, mousey = pygame.mouse.get_pos()
            pend.force(mousex, mousey, node)
         
        ev = pygame.event.get()

        for event in ev :
            if event.type == pygame.QUIT :
                running = False
            if stopped and event.type == pygame.MOUSEBUTTONDOWN :
                mousex, mousey = event.pos
                xpos, ypos = pend.getPos()
                radius = pend.getRadius()
                for i in range(len(xpos)) :
                    dist = (xpos[i] - mousex)**2 + (ypos[i] - mousey)**2
                    dist = np.sqrt(dist)
                    if dist < radius[i] :
                        forcing = True
                        node = i
            if event.type == pygame.MOUSEBUTTONUP :
                forcing = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED :
                if event.ui_element == gui.getStopButton() :
                    stopped = not gui.toggleStopButton()

            gui.processEvents(event)

        world.draw()
        gui.draw()
        gui.update(time_delta)

