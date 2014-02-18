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

    def __init__(self):
        '''
        Constructor
        '''
        self._cloud = None
        self._filename = ""
        self._outnum = 0
        self._time = 0.0
        self._snapdata = None
        self._type = "stars"
        self._billboarding = False
    
    def ChangeType(self, newtype):
        '''
        Change the type of fluid to show
        '''
        if newtype != self._type and newtype in self._types:
            self._type = newtype
            self.Open(self._filename)
        
    def Open(self, filename):
        '''
        Open a new snapshot
        '''
        self._filename = filename
        # Read data from filename
        #try:
        points, sizes, pointmass = self._LoadNewData(filename)
        #except:
        #    print "Open failed; returning..."
        #    return
        # Make drawable point cloud object
        if not self._cloud is None:
            del self._cloud
        if self._billboarding:
            self._cloud = BillboardDrawable(points,sizes,pointmass)
        else:
            self._cloud = SimpleDrawable(points,pointmass)
        
    def Draw(self, window):
        if not self._cloud is None:
            self._cloud.Draw(window)
            
    def InfoText(self):
        '''
        Return text giving information on the snapshot
        '''
        outnum = self._outnum
        time = self._time
        return "Output: "+str(outnum)+"\nTime: "+str(time)
            
    def _LoadNewData(self, filename):
        # Load data into pynbody
        print "STARTED LOADING DATA ", filename
        try:
            ro=pynbody.load(filename)
        except:
            print "ABORTING LOADING (Opening snapshot failed - does this file exist?)"
            return
        if self._type == "stars":
            fluid = ro.stars
        elif self._type == "gas":
            fluid = ro.gas
        elif self._type == "dm":
            fluid = ro.dm
        else:
            print "Fluid type",self._type," not recognised! Use stars, gas or dm."
            raise TypeError
        posns = fluid["pos"]
        # No points?
        if len(posns) <= 1:
            print "ABORTING LOADING (No stars)"
            return
        smooth = fluid["smooth"]
        if not type == "gas":
            mass = fluid["mass"]
        else:
            mass = fluid["mass"]*fluid["temp"] # Hacky! Mmm. Basically display thermal energy in an element?
        if type == "dm":
            mass *= 0.1 # Artificially lower the brightness
        # Cut off background gas to save on rendering
        if self._type == "gas":
            cutoff = 1e-3
            lim = mass > cutoff*np.max(mass)
            posns = posns[lim]
            smooth = smooth[lim]
            mass = mass[lim]
        # Process lengths to fit screen
        rescalepoints = False
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
        posns /= ro._info["boxlen"]
        smooth /= ro._info["boxlen"]
        posns -= 0.5
        #posns -= np.sum(posns,0)/len(posns)
        self._outnum = self._FindOutNum(filename)
        self._time = ro._info["time"]
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
 
