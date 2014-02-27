'''
Created on Feb 27, 2014

@author: sgeen
'''
# HACK SKETCH OF WHAT IT SHOULD LOOK LIKE

import pyglet
from pyglet.gl import *

import asvis
#from Frame import Frame
#from Snapshot import Snapshot

# Set up window
window = pyglet.window.Window(1024,1024)

# Add stuff
snap = asvis.Snapshot("spiral68_010")
stars = snap.MakeCloud("stars")

# Make frame in window
frame = asvis.Frame(window)
frame.Add(stars)

glClearColor(0.2, 0.4, 0.5, 1.0)

@window.event
def on_draw():
    # You can draw whatever pyglet stuff here
    # funnysprite.draw()
    # serioussprite.draw()
    # etc
    # IMPORTANT !! FRAME DRAW MUST CHECK THAT CAMERA, USER INPUT IS SET UP, 
    #              AND DO THAT IF NOT DONE ALREADY
    frame.Draw()
    # And you can do more stuff afterwards
    

pyglet.app.run()
