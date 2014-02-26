'''
Created on 17 Aug 2011

@author: samgeen
'''

import numpy
import numpy as np
import OpenGLStatics as Statics
from Display import Display
import Camera
from Input import Input
from MouseHandler import MouseHandler
from KeyHandler import KeyHandler
from PointDrawable import PointDrawable
from ColourShader import ColourShader

from Hamu.Octree import Octree

# Object library
from Hamu.PointCloud import PointCloud
from Maths.Vect3 import Vect3

# Pygame stuff
#import pygame
#import pygame.locals as pgl

class Visualisation(object):
    '''
    classdocs
    OpenGL visualisation toolkit
    NOTE: Parts of this class are static (thanks OpenGL)
    Bear this in mind when spawning multiple instances
    '''

    def __init__(self):
        self.__display = Statics.singletonDisplay
        self.__input = Statics.singletonInput
        
    # Start the display loop
    def StartDisplay(self):
        self.__display.Start()
        
    # Returns the display object
    def Display(self):
        return self.__display
    
def Run():
    # Make Gaussian point cloud
    testObject = PointCloud()
    mean = [0,0,0]
    cov = [[1.0,0,0],[0,1.0,0],[0,0,1.0]]*numpy.array([0.01])
    points = numpy.random.multivariate_normal(mean,cov,200000)
    print "Made points with shape", numpy.shape(points)
    testObject.AddPoints(numpy.array(points),numpy.zeros(len(points))+1.0) 
    cloud = PointDrawable(testObject)
    
    # Dump the point cloud into the display and start running it
    Visualisation().Display().AddObject(cloud)
    colourshader = ColourShader()
    Visualisation().Display().AddModifier(colourshader)
    Visualisation().StartDisplay()
     
     
def GadgetTest():
    # Read Gadget file
    '''
    file = open("/data/winhome/Data/Cosmocomp_Trieste/lowres/GasParticles.025")
    lines = file.readlines()
    points = numpy.zeros((len(lines),3))
    smooth = numpy.zeros((len(lines)))
    i = 0
    for line in lines:
        vals = line.split()
        points[i,0] = float(vals[0])
        points[i,1] = float(vals[1])
        points[i,2] = float(vals[2])
        smooth[i] = 1.0+float(i)/len(lines)#float(vals[16])
        i += 1
    print "Data read!", numpy.min(points), numpy.max(points)
    '''
    import pynbody
    #ro=pynbody.load("/data/Simulations/Disk/Runs/lvl10/output_00017")
    #ro=pynbody.load("/data/winhome/Data/Cosmocomp_Trieste/lowres/zoom.new_snap_025")
    print len(ro.stars["pos"])#
    print len(ro.gas["pos"])
    points = ro.gas["pos"]
    smooth = ro.gas["smooth"]
    print "Loading into visualiser"
    
    # Normalise points to +/- 1 and shift them to a mean of 0 in each axis
    minp = np.min(points,0)
    maxp = np.max(points,0)
    rangep = np.max(maxp-minp)
    points = points / rangep
    smooth /= rangep
    mean = numpy.mean(points,0)
    points -= mean
    print "Normalised data."
    
    # Make point cloud drawable object
    testObject = PointCloud()
    testObject.AddPoints(numpy.array(points),numpy.array(smooth))
    cloud = PointDrawable(testObject)
    
    # Dump the point cloud into the display and start running it
    colourshader = ColourShader()
    Visualisation().Display().AddObject(cloud)
    # NOTE! MEMORY LEAK IN CURRENT IMPLEMENTATION OF COLOUR SHADER!!!!
    Visualisation().Display().AddModifier(colourshader)
    Visualisation().StartDisplay()
    
def TestRamses():
    # Make Gaussian point cloud
    testObject = PointCloud()
    
    # Add Ramses particle data to it
    '''
    import pymses
    #ro = pymses.RamsesOutput("/data/Simulations/Disk/Runs/lvl10", 17)
    ro = pymses.RamsesOutput("/data/Simulations/Disk/Runs/JBLagrangian",86)
    part = ro.particle_source(["epoch","id"])
    '''
    import pynbody
    #ro=pynbody.load("/data/Simulations/Disk/Runs/lvl10/output_00017")
    ro=pynbody.load("/data/Simulations/Disk/Runs/JBLagrangian/output_00086")
    posns = ro.stars["pos"]
    smooth = ro.stars["smooth"]
    
    #try:
    #    for p in part:
    #        pass
    #except:
    #    print "No stars in this output!"
    #    import sys
    #    sys.exit()
    
    '''
    # HACK - Make Rtree
    # Load data into a simple list
    from rtree import index
    from rtree.index import Rtree
    props = index.Property()
    props.set_dimension(3)
    idx = index.Index(properties=props)
    points = np.array([])
    ids = np.array([])
    for p in part:
        stars = np.where(p["epoch"] > 0.0)
        parts = np.array(p.points)
        ids2 = p["id"]
        if points:
            points = np.concatenate(points,parts)
            ids = np.concatenate(ids,ids2)
        else:
            points = parts
            ids = ids2
    # Make tree
    for p, id in zip(points, ids):
        idx.add(id,(p[0],p[1],p[2]))
    # Now find rough kernel size
    partsize = np.zeros((ids.size))
    i = 0
    print "Finding kernel size..."
    for p, id in zip(points, ids):
        nNeighbours = 5
        neighbours = list(idx.nearest((p[0],p[1],p[2]), nNeighbours))
        dist = 0.0
        for n in neighbours:
            vect = p - points[np.where(ids == n)]
            dist += np.sum(vect*vect)
        partsize[i] = dist / (nNeighbours-1)
        i += 1
    print "Done"
    partsize = np.sqrt(partsize)
            
        
    
    # HACK ENDS
    '''
    '''
    for p in part:
        stars = np.where(p["epoch"] > 0.0)
        parts = np.array(p.points)
        print len(parts)
        posns = 5.0*(parts[stars] - 0.5)
        print len(posns)
        posns = numpy.array(posns)
        testObject.AddPoints(posns,smooth) 
    '''
    
    pmin, pmax = (np.min(posns),np.max(posns))
    posns = (posns - pmin) / (pmax - pmin)
    posns -= np.sum(posns,0)/len(posns)
    testObject.AddPoints(posns,smooth)
    cloud = PointDrawable(testObject)
    
    # Dump the point cloud into the display and start running it
    Visualisation().Display().AddObject(cloud)
    colourshader = ColourShader()
    Visualisation().Display().AddModifier(colourshader)
    Visualisation().StartDisplay()
     
if __name__ == "__main__":
    #GadgetTest()
    Run()
    #TestRamses()
