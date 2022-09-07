import abc
from abc import ABC, abstractmethod
from objects import World

class drawable(ABC) :
    def __init__(self, world=None) :
        self._world = world
    
    @abstractmethod
    def draw(self) :
        pass

    @abstractmethod
    def update(self) :
        pass

    def setWorld(self, world) :
        self._world = world
