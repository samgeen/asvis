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

    def __init__(self, window, x, y, width, height, camera=None):
        '''
        Constructor
        window - a pyglet window object
        x , y - position of bottom left corner of Frame in the window
        width, height - width and height of the frame
        camera - a camera object (default: will create a camera object for you)
        '''
        # Let's make these part of the interface why not
        # I'm sure this won't bite me in the ass later </irony>
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        AbstractFrame.__init__(self, window)
        self._drawables = []
        self._window = window
        if camera == None:
            camera = Camera.Camera(window)
        self._camera = camera
        self._renderer = Renderer.Renderer(self.Window(), camera)
        self._renderer.Redraw()
    
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
    
    def Camera(self, camera=None):
        # Switch the camera?
        if type(camera) != type(None):
            self._camera = camera
        # Return camera
        return self._camera
    
    def Draw(self, dummy=None):
        forceRedraw = False
        self._SetupView()
        if self._camera.ZoomActive():
            forceRedraw = True
        # HACK - ALWAYS REDRAW
        # TODO: REMOVE THIS!!!
        forceRedraw = True
        self._renderer.Draw(self._drawables, forceRedraw)
        
    def _SetupView(self):
        glViewport(self.x, self.y, self.width, self.height)
        self._camera.Draw()
