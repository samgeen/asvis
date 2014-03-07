'''
Created on Feb 27, 2014

@author: sgeen
'''
# HACK SKETCH OF WHAT IT SHOULD LOOK LIKE

import pyglet
from pyglet.gl import *

import asvis
import random
#from Frame import Frame
#from Snapshot import Snapshot

# Set up window
window = pyglet.window.Window(1024,1024)

# Add stuff
#snap = asvis.Snapshot("output_00016")
snap = asvis.Snapshot("spiral68_010")
stars = snap.MakeCloud("stars")

# Make frame in window
frames = list()
for i in range(0,5):
    size = random.randint(100,500)
    x = random.randint(0,window.width-size)
    y = random.randint(0,window.height-size)
    frame = asvis.Frame(window, x, y, size, size)
    frame.Add(stars)
    frames.append(frame)

glClearColor(0.2, 0.4, 0.5, 1.0)

@window.event
def on_draw():
    # You can draw whatever pyglet stuff here
    # funnysprite.draw()
    # serioussprite.draw()
    # etc
    # IMPORTANT !! FRAME DRAW MUST CHECK THAT CAMERA, USER INPUT IS SET UP, 
    #              AND DO THAT IF NOT DONE ALREADY
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    for frame in frames:
        frame.Draw()
    # And you can do more stuff afterwards
    

pyglet.app.run()
