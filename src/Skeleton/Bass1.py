from __future__ import print_function

import sys
import random


import Constants
import collections
import MusicTheory



prnFlag = True

class Bass1 ( ) : 
    '''

    '''

    def __init__ ( self, wbLevers, wbServerData ) :

        self.desc = 'bass1' 

        self.Chords = collections.OrderedDict()  # collection of Phrases
        self.Chords[0] = collections.OrderedDict()  # collection of chords within phrase
        for chId in range(len(wbServerData)) : 
            self.Chords[0][chId] =  wbServerData[str(chId)] 


        if ( 0 ) :
            print ( "Bass1 Data Phrase : 1" ) 
            for chId in self.Chords[0] : 
                print ( "\tChord Id: ", chId ) 
                for item in self.Chords[0][chId] : 
                    print ( "\t\tItem Num: 0 Data: ", item ) 
            print() 

