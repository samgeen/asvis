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
window = pyglet.window.Window(1900,1024)

# Test sprite
serious = pyglet.sprite.Sprite(pyglet.image.load('serious.png'), x=50, y=50)
silly = pyglet.sprite.Sprite(pyglet.image.load('silly.png'), x=window.width-550, y=50)

# Import simulation data
#snap = asvis.Snapshot("output_00016")
snap = asvis.Snapshot("spiral68_010")
stars = snap.MakeCloud("stars")

# Make frame in window
randFrames = True
if randFrames:
    frames = list()
    for i in range(0,5):
        size = random.randint(100,500)
        x = random.randint(0,window.width-size)
        y = random.randint(0,window.height-size)
        frame = asvis.Frame(window, x, y, size, size)
        frame.Add(stars)
        frames.append(frame)
else:
    frame = asvis.Frame(window, 200,200,512,512)
    frame.Add(stars)
    frames = [frame]

glClearColor(0.0, 0.0, 0.0, 1.0)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # You can draw whatever pyglet stuff here
    # funnysprite.draw()
    # serioussprite.draw()
    # etc
    serious.draw()
    # IMPORTANT !! FRAME DRAW MUST CHECK THAT CAMERA, USER INPUT IS SET UP, 
    #              AND DO THAT IF NOT DONE ALREADY
    for frame in frames:
        frame.Draw()
    # And you can do more stuff afterwards
    silly.draw()
    

pyglet.app.run()
