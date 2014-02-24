'''
Created on 17 Feb 2014

@author: samgeen
'''

import os, sys, pyglet
from pyglet.window import key, event
from pyglet.gl import * # it already has the gl prefix so OK whatevs

import Level as Level
import Events as Events
import Renderer as Renderer

class Window(pyglet.window.Window):
    # TODO: Use @ decorators and make this by composition instead!
    def __init__(self, *args, **kwargs):
        pyglet.window.Window.__init__(self, *args, **kwargs)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearDepth(1.0)
       
        # Clock
        self._clock = pyglet.clock.Clock()
        self._time = self._clock.time()
    
        # Stop pyglet burning a hole through the Earth's core with your cpu
        pyglet.clock.set_fps_limit(60)
        
        # EMPTY LEVEL
        self._level = None
            
    def ChangeLevel(self, nextLevel):
        '''
        Change the current level
        '''
        # Remove the last level's event handler
        #self.pop_handlers()
        # Setup the next level
        self._level = nextLevel
        print type(self._level)
        self._level.SetupWindow(self)

    def Player(self):
        '''
        Return the media player object
        '''
        return self._player

    def update(self):
        self.clear()
        
    def on_resize(self, width, height):
        # As suggested by zsprite.py
        # Based on the default with more useful clipping planes
        # NOTE - set clipping planes to +/- 1000 to avoid cutting out clipping
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, width, 0, height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def ScrollBy(self, dx, dy):
        # Scroll view by this amount
        x0, y0 = self._scrollpos
        self._scrollpos = (x0+dx,y0+dy)
        self.on_resize(self.width, self.height)
        
    def ScrollTo(self, x, y):
        # Scroll view to this position
        self._scrollpos = (x,y)
        self.on_resize(self.width, self.height)
            
    def Time(self):
        return self._clock.time()
            
    def on_draw(self,dt=0.0):

        dtime = self._clock.time() - self._time 
        self._time += dtime
        self._level.Draw()
        
    def on_key_press(self, symbol, modifiers):  
        '''
        Overload on_key_press to allow the level to clean up first
        '''      
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK | key.MOD_CAPSLOCK | key.MOD_SCROLLLOCK)):
            press = {"button":symbol, "mod": modifiers, "pressed":True}
            self._level.OnKeyboard(press)
            # Give the window a chance to tidy up
            self.dispatch_event('on_close')