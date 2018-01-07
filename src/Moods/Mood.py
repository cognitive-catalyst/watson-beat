from __future__ import print_function
from Skeleton import MusicTheory
from Skeleton import Constants

from PeruvianWaltz import *
from Anthematic import *
from Propulsion import *
from ReggaePop import *
from BomMarch import *
from Inspire import *
from PopFunk import *
from Chill import *
from Space import *
from Space_with_drums import *
from EDM import *

import os
import re
import sys
import math
import copy
import random
import collections


class Mood : 

    def __init__ ( self, movement, tempo ) : 
        
        if ( movement['mood'] == 'Inspire' or movement['mood'] == 'inspire' ) : 
            self.mood = Inspire ( movement, tempo ) 

        elif ( movement['mood'] == 'Anthematic' or movement['mood'] == 'anthematic' ) : 
            self.mood = Anthematic ( movement, tempo ) 

        elif ( movement['mood'] == 'Propulsion' or movement['mood'] == 'propulsion' ) : 
            self.mood = Propulsion ( movement, tempo ) 

        elif ( movement['mood'] == 'PeruvianWaltz' or movement['mood'] == 'peruvianwaltz' ) : 
            self.mood = PeruvianWaltz ( movement ) 

        elif ( movement['mood'] == 'BomMarch' or movement['mood'] == 'bommarch' ) : 
            self.mood = BomMarch ( movement, tempo ) 

        elif ( movement['mood'] == 'PopFunk' or movement['mood'] == 'popfunk' ) : 
            self.mood = PopFunk ( movement, tempo ) 

        elif ( movement['mood'] == 'ReggaePop' or movement['mood'] == 'reggaepop' ) : 
            self.mood = ReggaePop ( movement, tempo ) 
            
        elif ( movement['mood'] == 'Chill' or movement['mood'] == 'chill' ) : 
            self.mood = Chill ( movement, tempo ) 
            
        elif ( movement['mood'] == 'Space' or movement['mood'] == 'space' ) : 
            self.mood = Space ( movement, tempo )
            
        elif ( movement['mood'] == 'Space_with_drums' or movement['mood'] == 'space_with_drums' ) : 
            self.mood = Space_with_drums ( movement, tempo )
            
        elif ( movement['mood'] == 'EDM' or movement['mood'] == 'edm' ) : 
            self.mood = EDM ( movement, tempo )
            

