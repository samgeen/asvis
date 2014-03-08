'''
Created on 29 May 2012

@author: samgeen
'''

import pyglet
# Import straight into the global namespace because the "gl" prefix counts enough as a namespace-equivalent for us
from pyglet.gl import *
from pyglet.gl.glu import *
import ctypes, array
import numpy as np

from ReductionShader import ReductionShader
from Shader import Shader
    
class LogShader(object):
    '''
    Simple shader to project images in log space
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self._incShader = 0
        self._logShader = 0
        self._recalcMaxMin = 0 # Counter to recalculate max/min
        self._logmin = -16.11 # = ln(1e-7)
        self._invlogrng = 0.1 # arbitrary guess
        self._prepared = False # Has the shader been initialised?
        self._preloaded = False # Have we found the min/max value of the image?
        self._reduction = None # Reduction shader for calculating min/max
        
    # Do this when the program is loaded
    def Init(self):
        
        if not self._prepared:
            # Set up shaders
            self._incShader = Shader("IncrementBuffer")
            self._logShader = Shader("LogBuffer")
            '''
            self._reduction = ReductionShader(self._texture, max(self._width,self._height),
                                              ["ReduceMaxMin"])
            
            '''
            self._prepared = True
        
    # Do this before the objects are rendered
    def Begin(self):
        self._logShader.Bind()
        self._logShader.AddFloat(self._logmin, "texmin")
        self._logShader.AddFloat(self._invlogrng, "texinvrng")
        
        
    # Do this after the objects are rendered
    def End(self):
        self._logShader.Unbind()
        return
        # Take out the shader currently in use
        #self._incShader.Unbind()
        # Unbind frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        # TEST REDUCTION
        reduce = self._reduction.Run()
        maxval = reduce[0,0]
        minval = reduce[0,1]
        # Get the max/min value in the texture to pass to the shader
        self._recalcMaxMin -= 1
        properScale = self._recalcMaxMin <= 0
        properScale = True
        if properScale:
            #data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT)
            #red = data[:,:,0]
            #minval = np.min(red[np.nonzero(red)])
            #maxval = np.max(red)
            if minval == maxval:
                dmin = 0.0
                dmax = 0.0
                invrng = 1.0
            else:
                dmin = float(np.log(minval))
                dmax = float(np.log(maxval))
                #dmin = dmax - 10.0
                try:
                    invrng = 1.0/(dmax-dmin)
                except:
                    invrng = 1.0
            #print "Image min, range, max:", dmin, 1.0/invrng, dmax
            #newrng = np.min([10.0,1.0/invrng]) # HACK - stops weird hard circle effect
            #dmin = dmax - newrng
            #invrng = 1.0/newrng
            dmax = 3.0
            dmin = -3.0
            self._logmin = dmin
            self._invlogrng = invrng
            self._recalcMaxMin = 10
            #print self._logmin, self._invlogrng
            #del(data)
        # HACK
        #data = glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_FLOAT)
        #import scipy
        #scipy.misc.imsave('outfile.jpg', data)
        # HACK END
        
    def Reset(self):
        '''
        Reset the shader; make it run the pre-load operation again
        '''
        self._preloaded = False

