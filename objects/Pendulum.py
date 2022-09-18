import abc
from abc import ABC, abstractmethod
import numpy as np
import pygame
from objects import Physics
from objects import Drawable


class pendulum(Drawable.drawable) :
    def __init__(self, length, mass, theta, omega, phys, world) :
        super().__init__(world)
        self._length = length
        self._mass = mass
        self._theta = theta
        self._x = []
        self._y = []
        self._omega = omega
        for i in range(len(self._length)) :
            if i > 0 :
                self._x.append(self._x[i-1] + self._length[i] * np.sin(self._theta[i]))
                self._y.append(self._y[i-1] - self._length[i] * np.cos(self._theta[i]))
            else :
                self._x.append(self._length[i] * np.sin(self._theta[i]))
                self._y.append(-self._length[i] * np.cos(self._theta[i]))
        self._gravity = phys.gravity
        self._friction = phys.friction
        self._mountpoint_width = 0.1*world.getEffWidth()
        self._mountpoint_height = 0.05*world.getEffHeight()
        self._mass_radius = []
        for m in self._mass :
            self._mass_radius.append(20*m**(1./3.))
        self._method = euler(self)
        self._forcing_state = [False]*len(mass)
        tmargin, rmargin, bmargin, lmargin = self._world.getMargin()
        effwidth = self._world.getEffWidth()
        effheight = self._world.getEffHeight()
        origin_x = lmargin + round(effwidth/2.)
        origin_y = tmargin + self._mountpoint_height
        self._objectorigin = (origin_x, origin_y)

    def setNumMethod(self, method) :
        self._method = method

    def update(self, dt) :
        self._theta, self._omega = self._method.update(self._theta, self._omega, dt)
        for i in range(len(self._theta)) :
            self._x[i] = self._length[i] * np.sin(self._theta[i])
            self._y[i] = -self._length[i] * np.cos(self._theta[i])
            if i > 0 :
                self._x[i] = self._x[i] + self._x[i-1]
                self._y[i] = self._y[i] + self._y[i-1]

    def draw(self) :
        screenw = self._world.getEffWidth()
        screenh = self._world.getEffHeight()
        tmargin, rmargin, bmargin, lmargin = self._world.getMargin()

        screen = self._world.getScreen()

        for i in range(len(self._x)) :
            # mass circles
            x = self._x[i] / self._world.getScale() + lmargin + screenw/2
            y = -self._y[i] / self._world.getScale() + tmargin + self._mountpoint_height
            pygame.draw.circle(screen,
                               (0,0,255),
                               (x, y),
                               int(self._mass_radius[i]),
                               int(0.25*self._mass_radius[i]))
            # suspension
            if i > 0 :
                prev_x = self._x[i-1] / self._world.getScale() + lmargin + screenw/2
                prev_y = -self._y[i-1] / self._world.getScale() + tmargin + self._mountpoint_height
                sus_x1 = prev_x + int(self._mass_radius[i-1]*np.sin(self._theta[i]))
                sus_y1 = prev_y + int(self._mass_radius[i-1]*np.cos(self._theta[i]))
            else :
                sus_x1 = lmargin + screenw/2.
                sus_y1 = tmargin + self._mountpoint_height
            sus_x2 = x - int(self._mass_radius[i]*np.sin(self._theta[i]))
            sus_y2 = y - int(self._mass_radius[i]*np.cos(self._theta[i]))
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

    def force(self, fx, fy) :
        for node in range(self.getN()) :
            if self.isForced(node) :
                if node > 0 :
                    x0, y0 = self._x[node-1], self._y[node-1]
                else :
                    x0, y0 = 0, 0
                x0, y0 = self._world.convertWorldCoordinates((x0, y0), self._objectorigin)
                if fy - y0 > 0 :
                    theta = np.arctan((fx-x0)/(fy-y0))
                elif fy - y0 < 0 :
                    theta = np.pi + np.arctan((fx-x0)/(fy-y0))
                else :
                    theta = np.sign(fx-x0)*np.pi/2.
                self._theta[node] = theta
                self._omega = [0]*len(self._theta)
                self.update(0)

    def setForcingState(self, state, node) :
        self._forcing_state[node] = state

    def getPos(self) :
        posx, posy = [], []
        for i in range(len(self._x)) :
            px, py = self._world.convertWorldCoordinates((self._x[i], self._y[i]), self._objectorigin)
            posx.append(px)
            posy.append(py)
        return posx, posy

    def getRadius(self) :
        return self._mass_radius

    def getN(self) :
        return len(self._mass)

    def isForced(self, node) :
        return self._forcing_state[node]
        
    @abstractmethod
    def eom(self) :
        pass


class num_method(ABC) :
    def __init__(self, pendulum) :
        self._pendulum = pendulum
        
    @abstractmethod
    def update() :
        pass

    
class euler(num_method) :    
    def update(self, theta, omega, dt) :
        alpha = self._pendulum.eom(theta, omega)
        theta_new = []
        omega_new = []
        for i in range(len(theta)) :
            omega_new.append(omega[i] + alpha[i]*dt)
            theta_new.append(theta[i] + omega[i]*dt)
        return theta_new, omega_new

    
class rk4(num_method) :
    def update(self, theta, omega, dt) :
        k1 = self._pendulum.eom(theta, omega)
        thetamod = (np.array(theta) + 0.5*dt*np.array(k1)).tolist()
        k2 = self._pendulum.eom(thetamod, omega)
        thetamod = (np.array(theta) + 0.5*dt*np.array(k2)).tolist()
        k3 = self._pendulum.eom(thetamod, omega)
        thetamod = (np.array(theta) + dt*np.array(k3)).tolist()
        k4 = self._pendulum.eom(thetamod, omega)
        Phi = []
        omega_new = []
        theta_new = []
        for i in range(len(theta)) :
            Phi.append((k1[i] + 2*k2[i] + 2*k3[i] + k4[i])/6.)
            omega_new.append(omega[i] + Phi[i]*dt)
            theta_new.append(theta[i] + omega_new[i]*dt) # is this correct?
        return theta_new, omega_new

        
class pendulum1M(pendulum) :
    def eom(self, theta, omega) :
        alpha = self._gravity*np.sin(theta[0])/self._length[0] - self._friction*omega[0]
        return [alpha]

        
class pendulum2M(pendulum) :
    def eom(self, theta, omega) :
        # this is only valid for equal length and equal mass pendula
        alpha1 = (self._gravity/self._length[0])*(2*np.sin(theta[0]) - np.sin(theta[1])) - self._friction*omega[0]
        alpha2 = 2*(self._gravity/self._length[0])*(np.sin(theta[1]) - np.sin(theta[0])) - self._friction*omega[1]
        return [alpha1, alpha2]
