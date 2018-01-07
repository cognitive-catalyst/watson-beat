from __future__ import print_function

import sys
import random
import MusicTheory


TSERhythmInfo = {    
            
    '3/16' : {}, 
            
    '3/8'  : {}, 
    '4/8'  : {}, 
    '5/8'  : {}, 
    '6/8'  : {}, 
    '7/8'  : {}, 
    '9/8'  : {}, 
    '11/8' : {}, 
    '12/8' : {}, 
    '13/8' : {}, 
            
    '1/4' : { },
    '2/4' : { }, 
    '3/4' : { 'popRhythms' : { 'numBeats' : 12, 'beatAdderList' : [ 3, 6 ], 'startBeat': 1, 'resetBeat': 9, 'forbiddenBeat': 10 } },
    #'4/4' : { 'popRhythms' : { 'numBeats' : 16, 'beatAdderList' : [ 3, 6 ], 'startBeat': 1, 'resetBeat': 9, 'forbiddenBeat': 10 } },
    '4/4' : { 'popRhythms' : { 'numBeats' : 16, 'beatAdderList' : [ 2, 2, 2, 3, 3, 6 ], 'startBeat': 1, 'resetBeat': 9, 'forbiddenBeat': 10 } },
    '5/4' : { 'popRhythms' : { 'numBeats' : 20, 'beatAdderList' : [ 3, 6 ], 'startBeat': 1, 'resetBeat': 9, 'forbiddenBeat': 10 } },
    '6/4' : { 'popRhythms' : { 'numBeats' : 24, 'beatAdderList' : [ 3, 6 ], 'startBeat': 1, 'resetBeat': 9, 'forbiddenBeat': 10 } },
    '7/4' : { 'popRhythms' : { 'numBeats' : 24, 'beatAdderList' : [ 3, 6 ], 'startBeat': 1, 'resetBeat': 9, 'forbiddenBeat': 10 } },
            
            
    '2/2' : {}, 
    '3/2' : {}, 

}

