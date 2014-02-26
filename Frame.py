'''
Created on 24 Apr 2013

@author: samgeen
'''

import abc
import pyglet
from pyglet.gl import * # it already has the gl prefix so OK whatevs
import Events

import pyglet.window.mouse as mouse
import pyglet.window.key as key
import Camera
import Renderer
            
class AbstractFrame(object):
    '''
    A frame/sub-window containing a 3D scene
    '''
    __metaclass__ = abc.ABCMeta


    def __init__(self, window):
        '''
        Constructor
        '''
        self._window = window
        
    def Window(self):
        '''
        Get the current window instance
        '''
        return self._window
    
    @abc.abstractmethod
    def Setup(self):
        '''
        Setup the level
        ABSTRACT METHOD; MUST BE ADDED BY CONCRETE CLASS
        '''
        return
    
    @abc.abstractmethod
    def Draw(self):
        '''
        Draw the level
        ABSTRACT METHOD; MUST BE ADDED BY CONCRETE CLASS
        '''
        return
        
    # EVENT HANDLERS
    def OnMouseButton(self, state):
        '''
        Register the pressing or releasing of a mouse button
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"pos": (x,y), "button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        pass
    
    def OnMouseMove(self, state):
        '''
        Register the motion of the mouse
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"pos": (x,y), "button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        pass
    
    def OnKeyboard(self, state):
        '''
        Register the pressing or releasing of a keyboard key
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        pass
        
class Frame(AbstractFrame):
    '''
    The top level object for visualising astrophysics 
    '''

    def __init__(self, window, camera=None):
        '''
        Constructor
        '''
        Frame.Frame.__init__(self)
        self._drawables = []
        self._setup = False
        self._renderer = Renderer.Renderer(self.Window(), camera)
    
    def Add(self, drawable):
        '''
        Add drawable to frame
        '''
        self._drawables.append(drawable)
        
    def Remove(self, drawable):
        '''
        Remove drawable from frame
        '''
        self._drawables.remove(drawable)
    
    def Draw(self, dummy=None):
        if not self._setup:
            self.Setup()
        self._renderer.Draw(self._drawables)
        
    def OnMouseMove(self, state):
        '''
        Parse mouse movement
        '''
        if self._lmb:
            self._renderer.Camera().OnMouseMove(state)
        self.Redraw()

    def OnKeyboard(self, state):
        '''
        Register the pressing or releasing of a keyboard key
        This can be overridden by the concrete class if desired, or left inactive
        state - a dictionary of the mouse state:
                   {"button": button, "mod": modifier keys used, "pressed":True or False}
        '''
        # 113 = Q, 101 = e, YES I KNOW I'M IN A HURRY OK
        # Escape
        pressed = state["pressed"]
        button = state["button"]
        #if button == pyglet.window.key.ESCAPE:
            # Upon returning the window will now quit too
        # Q
        if button == pyglet.window.key.Q:
            self._renderer.Camera().ZoomIn(pressed)
        # E
        if button == pyglet.window.key.E:
            self._renderer.Camera().ZoomOut(pressed)
            
        # Switch render modes
        # TODO: Unbreak this
        #if button == pyglet.window.key.P and not pressed:
        #    self._renderer.ToggleBillboarding()
        
    def OnMouseButton(self, state):
        if state["button"] % 2 == pyglet.window.mouse.LEFT:
            self._lmb = state["pressed"] # True if pressed, False if not