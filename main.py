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
from objects import Event_Handler

class game_state :
    def __init__(self) :
        self.running = True
        self.stopped = True
        self.forcing = False

if __name__ == "__main__" :

    world = World.world()
    world.setRelMargin(0.1, 0.1, 0.1, 0.1)
    world.initPyGame()
    gui = GUI.pensimgui(world)
    
    phys = Physics.physics(friction=0.00)
    pend = Pendulum.pendulum2M(length=[0.4, 0.4],               
                                    mass=[1, 1],
                                    theta=[1.2, 2.3],
                                    omega=[0, 0],
                                    phys=phys,
                                    world=world)
    method = Pendulum.rk4(pend)
    pend.setNumMethod(method)
    world.appendObject(pend)

    pend2 = Pendulum.pendulum2M(length=[0.4, 0.4],               
                                    mass=[1, 1],
                                    theta=[1.2, 2.30001],
                                    omega=[0, 0],
                                    phys=phys,
                                    world=world)
    method = Pendulum.rk4(pend2)
    pend2.setNumMethod(method)
    world.appendObject(pend2)


    state = game_state()

    evt_handler = Event_Handler.pensim_event_handler(gui, world, state)

    clock = pygame.time.Clock()

    t0, t1 = 0, 0
    fps = 45
    num_time_interval = 1 # ms
    while state.running:
        time_delta = clock.tick(fps)

        if not state.stopped :
            tcyc = int(1000./fps)
            t0 = pygame.time.get_ticks()
            t1 = pygame.time.get_ticks()
            dt = 0
            while t1 - t0 < tcyc :
                t1 = pygame.time.get_ticks()
                world.update(dt/1000.)
                pygame.time.delay(num_time_interval)
                dt = pygame.time.get_ticks() - t1

        if state.forcing :
            mousex, mousey = pygame.mouse.get_pos()
            pendula = world.getObjectStack()
            pendula = [x for x in pendula if issubclass(type(x), Pendulum.pendulum)]
            for pend in pendula :
                for i in range(pend.getN()) :
                    if pend.isForced :
                        pend.force(mousex, mousey)

        ev = pygame.event.get()
        evt_handler.handleEvents(ev)

        world.draw()
        gui.draw()
        gui.update(time_delta)

