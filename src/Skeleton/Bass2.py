from __future__ import print_function

import sys
import random
import Constants

import MidiOutput
import MusicTheory
import BassActions

prnFlag = True

class Bass2 ( ) : 
    '''

    '''

    def __init__ ( self, wbLevers, scale, chord, duration, rhythm ) :

        self.desc = 'bass2' 
        self.duration = duration
        self.rhythm = rhythm
        self.homeChord = chord
        self.homeScale = scale
        self.id = wbLevers['id']


        layerParams = None
        # initialize actions for the bass2 layer 
        self.Actions = BassActions.Actions['bass2'][wbLevers['complexity']]
        self.numActions = len(self.Actions)



    def getNextNoteToBePlayed ( self, action ) : 

        octaveUp = False
        if ( action == 'PLAY_HOME_NOTE' ) : 
            nextNote = MusicTheory.AllChords[self.homeChord][0]

        elif ( action == 'PLAY_FIFTH_NOTE' ) : 
            nextNote = MusicTheory.AllChords[self.homeChord][2]

        elif ( action == 'PLAY_OCTAVE_UP' ) : 
            nextNote = MusicTheory.AllChords[self.homeChord][0]
            octaveUp = True

        elif ( action == 'PLAY_CHROMATICS' ) : 
            # LEFT for The Developer to be Filled in
            nextNote = MusicTheory.AllChords[self.homeChord][0]

        return [nextNote], octaveUp

    
    def run ( self ) : 
        totalActions = self.numActions - 1 # this is the total number of actions to choose from

        chosenItems = [] 
        for noteId in range(len(self.rhythm)) :

            chosenData     = {} 
            typeOfAction   = "Rnd"
            chosenReward   = 0 
            chosenDuration = self.rhythm[noteId] 

            if ( noteId == 0 ) :   # this is the first note to be played, so choose between home note and the octave up
                chosenAction = random.choice ( [ 'PLAY_HOME_NOTE', 'PLAY_OCTAVE_UP' ] )
            else : 
                chosenAction = self.Actions[ random.randint(0, totalActions) ] # not the first note. Choose any action
            chosenNote, octaveUp = self.getNextNoteToBePlayed  ( chosenAction )  

            chosenData = { 'action': chosenAction, 'notes':  chosenNote , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [chosenDuration], 'octaveUp': octaveUp } 
            chosenItems.append ( chosenData )

        if ( 0 ) : 
            for i in range(len(chosenItems)) : 
                print ( chosenItems[i]) 
            print() 

        return ( chosenItems ) 



