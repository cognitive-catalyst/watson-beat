from __future__ import print_function

import sys
import random
import Constants

import Constants
import MidiOutput
import MusicTheory
import collections

prnFlag = True

class BrassRhythm ( ) : 
    '''

    '''

    def __init__ ( self, wbLevers, scale, chord, duration, rhythm ) :

        self.desc = 'brassRhy' 
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


        if ( 0 ) : 
            for rhy in self.rhythm : 
                print ( self.rhythm[rhy] ) 


    def run ( self ) : 


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
            
            if ( 0 ) : #and mNum > 0 and muteMeasure ) : 
                chosenData = {} 
                chosenData = {  'notes':  ['C'] , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [Constants.TSEs[self.tse]['oneMeasure']], 'octaveUp': False, 'velocity': 0 } 
                chosenItems.append ( chosenData )
                continue


            for beat in self.rhythm :

                if ( halfMeasureChord and beat >= halfMeasureBeat ) : 
                    break 

                chosenData     = {} 
                if (  0 ) : # and beat >= halfMeasureBeat and muteHalfMeasure ) : 
                    chosenDuration = (  numBeats+1 - beat )  *  Constants.NoteDurationDict['sixteenth']
                    chosenData = { 'action': 'PLAY_HOME_NOTE', 'notes':  ['C'] , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [chosenDuration], 'octaveUp': False, 'velocity': 0 } 
                    chosenItems.append ( chosenData )
                    break

              
                midiClk  = 0 
                midiAdder = 0 
                numChordTones = len(MusicTheory.AllChords[self.homeChord] ) 
              
                velocity = self.rhythm[beat]['velocity']
                duration = self.rhythm[beat]['duration']
                #print ( "velocity: ", velocity, "duration: ", duration )
                    
                notes = []
                octaves = [] 
                for noteNum in range( 0, numChordTones ): 
                    if ( noteNum == 0 ) : 
                        octave = 6                        
                        while  ( True ) : 
                            chordToneIndex = random.randint ( 0 , numChordTones-1 ) 
                            note = MusicTheory.AllChords[self.homeChord][chordToneIndex] 
                            pitch  = MusicTheory.NotesToPitch[note] + ( octave*12 ) 

                            if ( pitch <= 81 ) : 
                                break 
                        prevPitch = 1000
                                                
                    note = MusicTheory.AllChords[self.homeChord][chordToneIndex] 
                    pitch  = MusicTheory.NotesToPitch[note] + ( octave*12 ) 
                    if ( prevPitch < pitch ) : 
                        octave -= 1
                        pitch -= 12

                    midiPitchStr = 'midi.' + note + "_" + str(octave) 

                    notes.append ( note ) 
                    octaves.append ( octave ) 
                    if ( velocity > 50 ) : 
                        velocity -= random.randint ( 1, 10  ) 
                        
                    chosenData =  { 'event': 'on',  'notes': [note], 'midiClk': midiClk, 'pitch': midiPitchStr, 'pitches': [pitch], 'chord': self.homeChord, 'scale': self.homeScale, 'duration': duration, 'octaves': [octave],  'velocity': velocity } 
                    chosenItems.append ( chosenData )

                    midiAdder += midiClk                    
                    midiClk = 0 #random.randint(5, 15 ) 

                    chordToneIndex -= 1
                    if ( chordToneIndex < 0 ) : 
                        chordToneIndex = numChordTones - 1
                    prevPitch = pitch
                        

                for noteNum in range( 0, numChordTones ): 
                    if ( noteNum == 0 ) : 
                        midiClk = duration - midiAdder
                    else : 
                        midiClk = 0 

                    note   = notes[noteNum] 
                    octave = octaves[noteNum] 
                    midiPitchStr = 'midi.' + note + "_" + str(octave) 
                    pitch  = MusicTheory.NotesToPitch[note] + ( octave*12 ) 


                    chosenData =  { 'event': 'off',  'notes': [note], 'midiClk': midiClk, 'pitch': midiPitchStr, 'pitches': [pitch], 'chord': self.homeChord, 'scale': self.homeScale, 'duration': duration, 'octaves': [octave],  'velocity': 0} 
                    chosenItems.append ( chosenData )

                    

        if ( 0 ) : 

            for i in range(len(chosenItems)) : 
                print ( chosenItems[i]) 
            print() 


        return ( chosenItems ) 
