'''
Created on 1 Oct 2013

@author: samgeen
'''

from pyglet.gl import *
import numpy as np

class SimpleDrawable(object):
    '''
    A simple test object
    '''
    def __init__(self,points,mass):
        '''
        Constructor
        '''
        flat = points.flatten()
        self._masses = mass
        self._colours = None
        self._pointsGL = (GLfloat * len(flat))(*flat)
        self._window = 0
        self._first = True
        
    # Draw the points to screen
    def Draw(self, window):
        '''
        Draw object
        '''
        self._window = window
        
        # First time through?
        # NOTE: I have no idea how reliable this code is at determining whether we set these things
        if self._first:
            m = np.array([self._masses])
            m /= m.max()
            # HACK
            #m *= 0.0
            #m += 1.0
            # HACK END
            c = np.array([1.0,1.0,1.0,1.0])
            flat = (c * m.T).flatten()
            self._colours = (GLfloat * len(flat))(*flat)
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
            glVertexPointer(3, GL_FLOAT, 0, self._pointsGL)
            glColorPointer(4,GL_FLOAT,0,self._colours)
            self._first = False
            
        glPointSize(5.0)
        glDrawArrays(GL_POINTS, 0, len(self._pointsGL) // 3)
        #glBegin(GL_POINTS)
        #for it in self._points:
        #    glVertex3f(it[0],it[1],it[2])
        #glEnd()
        # DIAGNOSTIC PRINT
        #print "Number points shown:", len(self._pointsGL) // 3
            