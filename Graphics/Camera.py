'''
Created on 15 Aug 2011

@author: samgeen
'''

' TODO: CREATE POLYMORPHIC INTERFACE!!! '

import pyglet
from pyglet.gl import *
from pyglet.gl.glu import *

import numpy as np

#import EventHandler as Events
#from MouseHandler import MouseHandler
import math

from Maths.Vect3 import Vect3
from Maths.Quaternion import Rotation

import Events

class Camera(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        zoomInit = 1.0
        self.__zoom = zoomInit
        self.__lookAt = Vect3(0.0,0.0,0.0)
        self.__position = Vect3(0.0,0.0,zoomInit)
        self.__up = Vect3(0.0,1.0,0.0)
        self.__right = Vect3(1.0,0.0,0.0) # This is reset during the view calculations
        self.__xangle = 0.0
        self.__yangle = 0.0
        self.__zoomSpeed = 1.30
        # Keep track of time for smooth moving of camera
        self._clock = pyglet.clock.Clock()
        self._time = self._clock.time()
        self._prevtime = self._time
        self._zoomIn = False
        self._zoomOut = False
        ' Events '
        #self.__inputHandler = MouseHandler()
        #self.__inputHandler.RegisterEvents()
        #Events.RegisterEvent("CAMERA_ROTATE", self.Rotate)
        #Events.RegisterEvent("CAMERA_ZOOM_IN", self.ZoomIn)
        #Events.RegisterEvent("CAMERA_ZOOM_OUT", self.ZoomOut)
        # PREVIOUS MOUSE POSITIONS
        self.__oldscrx = 0
        self.__oldscry = 0
        
    def OnMouseMove(self, state):
        '''
        Parse mouse movement
        '''
        x, y = state["pos"]
        # Good speed for a mouse
        rotateSpeed = 5e-2
        # Good speed for a wiimote
        rotateSpeed = 2e-2
        xangle = -(x - self.__oldscrx) * rotateSpeed
        yangle = (y - self.__oldscry) * rotateSpeed
        self.__oldscrx = x
        self.__oldscry = y
        self.Rotate((xangle, yangle))
        
    def Rotate(self, angles):
        self.__xangle += angles[0]
        self.__yangle += angles[1]
        # Find total angle
        angle = math.sqrt(angles[0]*angles[0] + angles[1]*angles[1])
        # Make sure the right-pointing vector is set properly (as cross product of up and lookAt)
        self.__right = -self.__up ^ self.__position.Normal()
        # Find direction the angle displacement is pointing
        displacement = self.__right*angles[0] + self.__up*angles[1]
        # Now find the vector perpendicular to that and the camera direction
        vector = -self.__position ^ displacement
        # Now ROTATE
        if vector.LengthSqrd() > 0:
            rotation = Rotation(angle, vector)
            self.__position = rotation.RotateVector(self.__position)
            self.__up = rotation.RotateVector(self.__up)
        # Done!
        
        '''
        from math import cos
        from math import sin
        import numpy as np
        import pdb
        # Build rotation matrices
        x = angles[0]
        y = angles[1]
        cx = cos(x)
        cy = cos(y)
        sx = sin(x)
        sy = sin(y)
        rx = np.matrix([[cx,-sx,0],[sx,cx,0],[0,0,1]])
        ry = np.matrix([[cy,0,-sy],[0,1,0],[sy,0,cy]])
        pos = np.matrix([self.__position[0],self.__position[1],self.__position[2]])
        up = np.matrix([self.__up[0],self.__up[1],self.__up[2]])
        newpos = ry*rx*pos.T
        newup = ry*rx*up.T
        self.__position = Vect3(newpos[0,0],newpos[1,0],newpos[2,0])
        self.__up = Vect3(newup[0,0],newup[1,0],newup[2,0])
        '''
        self._RecalculatePosition()
            
    def Zoom(self, zoom=None):
        '''
        Set zoom or return its current value (or both)
        '''
        if zoom:
            self.__position *= zoom / self.__zoom
            self.__zoom = zoom
            self._RecalculatePosition()
        return self.__zoom
    
    def ZoomActive(self):
        '''
        HACK - Is the zoom currently active?
        '''
        return self._zoomIn or self._zoomOut
            
    def ZoomIn(self, on=True):
        '''
        Zoom in camera
        '''
        self._zoomIn = on
        
    def ZoomOut(self, on=True):
        '''
        Zoom in camera
        '''
        self._zoomOut = on
    
    def _RecalculatePosition(self):
        
        #self.__position[0] = self.__zoom*math.cos(self.__xangle) * math.sin(self.__yangle)
        #self.__position[1] = self.__zoom*math.sin(self.__xangle) * math.sin(self.__yangle)
        #self.__position[2] = self.__zoom*math.cos(self.__yangle)
        Events.Redraw()
        # TODO; REMOVE THIS PLUMBING TO THE OLD EVENT HANDLER
        #Events.FireEvent("REDRAW",0)
    
    def Draw(self):
        '''
        Update the display with the current camera view
        '''
        self._prevtime = self._time
        self._time = self._clock.time()
        dt = self._time - self._prevtime
        self._CalcZoom(dt)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45,1.0,0.0001,10.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.__position[0], self.__position[1], self.__position[2], 
                  self.__lookAt[0], self.__lookAt[1], self.__lookAt[2], 
                  self.__up[0], self.__up[1], self.__up[2])
        
    def LookAt(self, point):
        '''
        Set point to look at
        '''
        self.__lookAt = point
        
    def Position(self, point=0):
        '''
        Set/get position of camera
        '''
        if type(point) == type(0):
            return self.__position
        else:
            self.__position = point
        
    def Up(self, direction):
        '''
        Give direction of up
        '''
        self.__up = direction
        
    def _CalcZoom(self, dt):
        # The zoom is a logarithmic zoom, i.e. zooms by factors of 10 in constant time
        zoomfact = self.__zoomSpeed ** dt
        if self._zoomIn:
            self.__zoom /= zoomfact
            self.__position /= zoomfact
        if self._zoomOut:
            self.__zoom *= zoomfact
            self.__position *= zoomfact
        #print self.__zoom, dt
        #if self._zoomIn or self._zoomOut:   
        self._RecalculatePosition()
