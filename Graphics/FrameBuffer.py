'''
Created on 29 May 2012

@author: samgeen
'''

import pyglet
from pyglet.gl import *
from pyglet.gl.glu import *
import ctypes, array
import numpy as np

    
class FrameBuffer(object):
    '''
    Framebuffer object designed to store rendered object as a texture for later manipulation
    '''


    def __init__(self, width, height):
        '''
        Constructor
        '''
        self._width, self._height = (width, height)
        self._depth = 0#ctypes.c_int(0)
        self._frame = 0#ctypes.c_int(0)
        self._texture = 0#ctypes.c_int(0)
        self._image = 0
        self._prepared = False
        
    # Do this when the program is loaded
    def Init(self):
        
        if not self._prepared:
            # Set up image 
            
            # Set up empty texture to draw to
            self._texture = ctypes.c_uint(0)
            glGenTextures(1,self._texture)
            #self._texture = pyglet.image.Texture.create(self._width, self._height, rectangle=True,internalformat=GL_RGBA32F_ARB)
            
            glEnable( GL_TEXTURE_2D )
            glBindTexture( GL_TEXTURE_2D, self._texture )
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glPixelStorei(GL_UNPACK_ROW_LENGTH, 0)
            glPixelStorei(GL_UNPACK_SKIP_PIXELS, 0)
            glPixelStorei(GL_UNPACK_SKIP_ROWS, 0)
            
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F_ARB, self._width, self._height, 0,\
             GL_RGBA, GL_FLOAT, 0)
            #glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self._width, self._height, 0,\
            # GL_RGBA, GL_UNSIGNED_BYTE, 0)
            glBindTexture(GL_TEXTURE_2D, 0)
            
            # Set up the frame buffer object
            self._frame = ctypes.c_uint(0)
            glGenFramebuffers(1,self._frame)
            #self._frame = glGenFramebuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER, self._frame)
            
            # Set up the depth buffer
            #self._depth = glGenRenderbuffers(1)
            self._depth = ctypes.c_uint(0)
            glGenRenderbuffers(1,self._depth)
            glBindRenderbuffer(GL_RENDERBUFFER, self._depth)
            
            glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self._width, self._height)
            glBindRenderbuffer(GL_RENDERBUFFER, 0)
            
            # Attach texture and depth buffer
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self._texture, ctypes.c_int(0))
            glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self._depth)
            
            # Unbind frame buffer for now
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
            status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
            print "FRAME BUFFER STATUS:", status
            
            self._prepared = True
        
    # Do this before the objects are rendered
    def Begin(self):
        
        # Re-bind frame buffer
        self.Init()
        glBindFramebuffer(GL_FRAMEBUFFER, self._frame)
        
        # Clear frame buffer
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glDisable( GL_TEXTURE_2D )
        glViewport(0,0,self._width, self._height)
        # At this point we draw the scene
        
    # Do this after the objects are rendered
    def End(self):
        # Unbind frame buffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def DrawTexture(self):
        # Now we need to plot the texture to screen
        # Set up an orthogonal projection
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glDisable(GL_BLEND)
        #glDrawPixels(self._width, self._height, GL_RGBA, GL_FLOAT, self._texture)
        # Now draw the texture with the log shader
        # Draw the texture onto a flat plane
        glColor4f(1.0,1.0,1.0,1.0)
        glEnable( GL_TEXTURE_2D )
        #glDisable(GL_TEXTURE_GEN_S)
        #glDisable(GL_TEXTURE_GEN_T)
        glBindTexture( GL_TEXTURE_2D, self._texture )
        glBegin(GL_TRIANGLES)
        glTexCoord2d(0.0,0.0);        glVertex3f(0.0, 0.0, 0.0);
        glTexCoord2d(1.0,0.0);        glVertex3f(1.0, 0.0, 0.0);
        glTexCoord2d(1.0,1.0);        glVertex3f(1.0, 1.0, 0.0);
        
        glTexCoord2d(1.0,1.0);        glVertex3f(1.0, 1.0, 0.0);
        glTexCoord2d(0.0,1.0);        glVertex3f(0.0, 1.0, 0.0);
        glTexCoord2d(0.0,0.0);        glVertex3f(0.0, 0.0, 0.0);
        glEnd()
        glBindTexture( GL_TEXTURE_2D, 0 )
        

