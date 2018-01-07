from __future__ import print_function
#from RL import State
#from RL import QLearning
from RL import StateAttributes
from RL import ComplexityKnobs

import sys
import random
import Constants

import Constants
import MidiOutput
import MusicTheory
import Environment
import collections

prnFlag = True

class Bass3 ( ) : 
    '''

    '''

    def __init__ ( self, wbLevers, scale, chord, duration, rhythm ) :

        self.desc = 'bass3' 
        self.duration = duration
        self.homeChord = chord
        self.rhythm = rhythm
        self.homeScale = scale
        self.id = wbLevers['id']
        self.tse = wbLevers['tse']

        # initialize the state attributes for the bass2 layer
        #self.StateAttributes = StateAttributes.StateAttributes[self.desc]
        #self.numFeatures     = len( self.StateAttributes ) 
        #self.features        = [ i for i in range(self.numFeatures) ]



        layerParams = None
        # initialize actions for the bass2 layer 
        self.Knobs, self.Actions, self.ReverseActions = ComplexityKnobs.setKnobs ( self.desc, wbLevers['complexity'], layerParams ) 
        self.numActions = len(self.Actions)


        if ( 0 ) : 
            for rhy in self.rhythm : 
                print ( self.rhythm[rhy] ) 
                

    def run ( self ) : 
        totalActions = self.numActions - 1 # this is the total number of actions to choose from

        numBeats = Constants.TSEs[self.tse]['num16thBeats'] 

        halfMeasureChord = False

        numMeasures     = self.duration // Constants.TSEs[self.tse]['oneMeasure'] 
        halfMeasureBeat = ( numBeats // 2 ) + 1 

        if ( 0 ) : 
            print ( "self.duration: :", self.duration, "Num Beats: ", numBeats, "Num Measures: ", numMeasures, "halfMeasurebeat: ", halfMeasureBeat, self.rhythm ) 

        if ( numMeasures == 0 ) : 
            numMeasures = 1
            chordDuration = self.duration
            halfMeasureChord = True

        chosenItems = [] 
        for mNum in range( numMeasures ) : 

            if random.randint ( 0, 100 ) > 50 : 
                muteMeasure = True
            else : 
                muteMeasure = False

            if random.randint ( 0, 100 ) > 70 : 
                muteHalfMeasure = True
            else : 
                muteHalfMeasure = False
            
            if ( mNum > 0 and muteMeasure ) : 
                chosenData = {} 
                chosenData = { 'action': 'PLAY_HOME_NOTE', 'notes':  ['C'] , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [Constants.TSEs[self.tse]['oneMeasure']], 'octaveUp': False, 'velocity': 0 } 
                chosenItems.append ( chosenData )
                continue


            for beat in self.rhythm :

                if ( halfMeasureChord and beat >= halfMeasureBeat ) : 
                    break 

                chosenData     = {} 
                if (  beat >= halfMeasureBeat and muteHalfMeasure ) : 
                    chosenDuration = (  numBeats+1 - beat )  *  Constants.NoteDurationDict['sixteenth']
                    chosenData = { 'action': 'PLAY_HOME_NOTE', 'notes':  ['C'] , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [chosenDuration], 'octaveUp': False, 'velocity': 0 } 
                    chosenItems.append ( chosenData )
                    break

                typeOfAction   = "Rnd"

                velocity       = self.rhythm[beat]['velocity']              
                chosenDuration = self.rhythm[beat]['duration'] 

                if ( beat == 0 ) :   # this is the first note to be played, so choose between home note and the octave up
                    chosenAction = random.choice ( [ 'PLAY_HOME_NOTE', 'PLAY_OCTAVE_UP' ] )
                else : 
                    chosenAction = self.Actions[ random.randint(0, totalActions) ] # not the first note. Choose any action
                chosenNote, octaveUp = self.getNextNoteToBePlayed  ( chosenAction )  
                
                chosenData = { 'action': chosenAction, 'notes':  chosenNote , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [chosenDuration], 'octaveUp': octaveUp, 'velocity': velocity } 
                chosenItems.append ( chosenData )

        if ( 0 ) : 
            for i in range(len(chosenItems)) : 
                print ( chosenItems[i]) 
            print() 

        return ( chosenItems ) 

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
            # FIX ME
            nextNote = MusicTheory.AllChords[self.homeChord][0]

        return [nextNote], octaveUp



def getRhyDurations ( rhyOption, tse ) : 

    rhythm = collections.OrderedDict() 

    numBeats = Constants.TSEs[tse]['num16thBeats'] 
    if ( 0 ) : 
        print ( rhyOption ) 

    for beatIndex, beat in enumerate(rhyOption)  : 

        if ( not isinstance( beat, int ) ) :  # Rest Note
            velocity = 0 
            beat = int( beat.replace ( "Rest", '' ) )
            rhyOption[beatIndex] = beat 
        else : 
            velocity = random.randint ( 60, 100) 



        if ( beatIndex == len(rhyOption) - 1 ) : # last notes
            chosenDuration = (  numBeats+1 - beat )  *  Constants.NoteDurationDict['sixteenth']
        else : 

            if ( not isinstance( rhyOption[beatIndex+1], int ) ) :  # Rest Note                
                nextBeat = int( rhyOption[beatIndex+1].replace ( "Rest", '' ) )
            else : 
                nextBeat = rhyOption[beatIndex+1]
        
            chosenDuration = (  nextBeat - beat )  *  Constants.NoteDurationDict['sixteenth']


        if ( chosenDuration >= Constants.NoteDurationDict['eighth'] and chosenDuration < Constants.NoteDurationDict['quarter'] ) : 
            if ( random.randint ( 0, 100 ) > 50 ) :  # split into 16th note + 16th note Rest
                rhythm[beat]   = {  'velocity': velocity, 'duration': Constants.NoteDurationDict['sixteenth'] }
                remainingDuration = chosenDuration -Constants.NoteDurationDict['sixteenth'] 
                rhythm[beat+1] = { 'velocity': 0, 'duration': remainingDuration }
            else : 
                rhythm[beat]   = {  'velocity': velocity, 'duration': chosenDuration } 
        elif ( chosenDuration >= Constants.NoteDurationDict['quarter'] ) : 
            if ( random.randint ( 0, 100 ) > 70 ) :  # split into 16th note + Rest, or 8th note + Rest or quarter note + rest 
                duration = random.choice ( [ (Constants.NoteDurationDict['sixteenth'], 1) , (Constants.NoteDurationDict['eighth'],2), (Constants.NoteDurationDict['quarter'],4) ] )                   
                rhythm[beat]   = {  'velocity': velocity, 'duration': duration[0] }
                remainingDuration = chosenDuration - duration[0] 
                rhythm[beat+duration[1] ] = { 'velocity': 0, 'duration': remainingDuration } 
            else : 
                rhythm[beat]   = {  'velocity': velocity, 'duration': chosenDuration } 
        else : 
            rhythm[beat]   = {  'velocity': velocity, 'duration': chosenDuration }

            
            
    if ( 0 ) : 
        for beat in rhythm :
            print ( "Beat: ", beat,  "duration: ", rhythm[beat]['duration'] ,  "velocity: ", rhythm[beat]['velocity'] ) 

    return rhythm



