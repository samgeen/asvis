'''
Created on 6 Dec 2013

@author: samgeen
'''

import os
import pyglet
import pynbody
import numpy as np
#from Graphics.PointDrawable import PointDrawable
from Graphics.SimpleDrawable import SimpleDrawable
from Graphics.BillboardDrawable import BillboardDrawable

class Snapshot(object):
    '''
    Handles the simulation data from a single snapshot and renders it
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self._outnum = 0
        self._time = 0.0
        self._billboarding = False
        self._snapdata = None
        self._filename = filename
        
    def MakeCloud(self, fluidtype):
        '''
        Open a new snapshot
        '''
        # Read data from filename
        points, sizes, pointmass = self._LoadNewData(fluidtype)
        # Make drawable point cloud object
        if self._billboarding:
            cloud = BillboardDrawable(points,sizes,pointmass)
        else:
            cloud = SimpleDrawable(points,pointmass)
        return cloud
            
    def InfoText(self):
        '''
        Return text giving information on the snapshot
        '''
        outnum = self._outnum
        time = self._time
        return "Output: "+str(outnum)+"\nTime: "+str(time)
            
    def _LoadNewData(self, fluidtype):
        # Load data into pynbody
        print "STARTED LOADING DATA ", self._filename
        ro = self._snapdata
        if ro == None:
            try:
                ro=pynbody.load(self._filename)
            except:
                print "ABORTING LOADING (Opening snapshot failed - does this file exist?)"
                return
        if fluidtype == "stars":
            fluid = ro.stars
        elif fluidtype == "gas":
            fluid = ro.gas
        elif fluidtype == "dm":
            fluid = ro.dm
        else:
            print "Fluid type",fluidtype," not recognised! Use stars, gas or dm."
            raise TypeError
        posns = fluid["pos"]
        # No points?
        if len(posns) <= 1:
            print "ABORTING LOADING (No stars)"
            return
        smooth = fluid["smooth"]
        if not fluidtype == "gas":
            mass = fluid["mass"]
        else:
            mass = fluid["mass"]*fluid["temp"] # Hacky! Mmm. Basically display thermal energy in an element?
        if fluidtype == "dm":
            mass *= 0.1 # Artificially lower the brightness
        # Cut off background gas to save on rendering
        if fluidtype == "gas":
            cutoff = 1e-3
            lim = mass > cutoff*np.max(mass)
            posns = posns[lim]
            smooth = smooth[lim]
            mass = mass[lim]
        # Process lengths to fit screen
        rescalepoints = True
        if rescalepoints:
            pmin, pmax = (np.min(posns),np.max(posns))
            posns = (posns - pmin) / (pmax - pmin)
            smooth /= (pmax - pmin)
        if smooth.max() <= 0.0:
            smooth *= 0.0
            smooth += 1.0
        else:
            smooth[smooth <= 0.0] = smooth[smooth > 0.0].min()
        cheaprescale = False
        if cheaprescale:
            cheap = fluid["pos"].units
            posns /= cheap
            smooth /= cheap
        posns -= 0.5
        self._outnum = 0#self._FindOutNum(filename)
        self._time = 0.0#ro._info["time"]
        self._snapdata = ro
        print "DONE LOADING DATA"
        return posns, smooth, mass
        
    def _FindOutNum(self, string):
        '''
        Find the RAMSES output number in a string containing the file path
        '''
        numpos = string.index("output_")+len("output_")
        numstr = string[numpos:numpos+5]
        return int(numstr)
 
