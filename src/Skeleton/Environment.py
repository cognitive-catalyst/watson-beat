from __future__ import print_function

import sys
import copy 

import Constants
import MusicTheory
import ChordProgressions
import ChordProgressionsInspired
    
class Environment :

    def __init__ (self, tse, pl, scale, chord ) : 
        
        self.tse = tse
        self.phraseLength = pl
                
        self.maxduration = Constants.TSEs[tse]['oneMeasure'] * pl 
        self.maxMeasures = pl 

        self.primaryScale = scale 
        self.homeChord    = chord


    def InitializeEnvironment ( self, scale ) :         

        self.currentChord  = self.homeChord
        self.previousChord = self.homeChord

        self.currentScale  = scale
        self.previousScale = scale
            

    def printEnvironmentVariables ( self ) : 
        print ( "\nEnvironment Variables" ) 

        print ( "Primary Scale   : ", self.primaryScale ) 
        print ( "Home Chord      : ", self.homeChord ) 

        print ( "Current  Chord  : ", self.currentChord ) 
        #print ( "Previous Chord  : ", self.previousChord )

        print ( "Current  Scale  : ", self.currentScale ) 
        #print ( "Previous Scale  : ", self.previousScale )
    
        print ( "Time Signature  : ", self.tse ) 



class Bass2Environment ( Environment ) : 

    def __init__ (self, tse, pl, scale, chord) : 

        Environment.__init__(self, tse, pl, scale, chord ) 

        self.durationChordTonesForChordLength    = 0.0 
        self.durationNonChordTonesForChordLength = 0.0 

    def InitializeEnvironment ( self, scale ) : 

        Environment.InitializeEnvironment ( self, scale ) 
        self.durationChordTonesForChordLength    = 0.0 
        self.durationNonChordTonesForChordLength = 0.0 
        
    def printEnvironmentVariables ( self ) :        

        Environment.printEnvironmentVariables ( self ) 
        print ( "Duration of Chord Tones    : ", self.durationChordTonesForChordLength ) 
        print ( "Duration of Non Chord Tones: ", self.durationNonChordTonesForChordLength ) 

    def updateStateParams ( self, action, data ) :         

        note = data['notes'] 
        duration = data['duration'] 
        numNotes = len(note) 
        for i in range(numNotes) : 
            
            if ( note[i] in MusicTheory.AllChords[self.currentChord] ) :  
                self.durationChordTonesForChordLength += duration[i] 

            elif ( note[i] not in MusicTheory.AllChords[self.currentChord] ) : 
                self.durationNonChordTonesForChordLength += duration[i] 
                


class Bass1Environment ( Environment ) : 

    def __init__ (self, tse, pl, scale, mood) : 

        Environment.__init__(self, tse, pl, scale, scale ) 

        self.chordProgressionPenalty = 0.0 
        #initialize chord progressions
        self.cpJumps = ChordProgressions.ChordProgressionJumps ( self.primaryScale ) 

        if ( 0 ) : 
            self.cpJumps.printChordProgressions() 
            sys.exit(0) 

    def InitializeEnvironment ( self, scale ) : 

        Environment.InitializeEnvironment ( self, scale ) 
        

    def printEnvironmentVariables ( self ) :        

        Environment.printEnvironmentVariables ( self ) 
        

    def updateStateParams ( self, action, data ) : 
        chord = data['chord']
        scale = data['scale']
        penalty = data['penalty']

        self.previousChord = self.currentChord                       
        self.currentChord  = chord
        
        self.previousScale = self.currentScale 
        self.currentScale  = scale

        self.homeChordMovementDistance = penalty 



class Melody5Environment ( Environment ) : 

    def __init__ (self, tse, pl, scale, chord) : 

        Environment.__init__(self, tse, pl, scale, chord ) 

        self.durationChordTonesForChordLength    = 0.0 
        self.durationNonChordTonesForChordLength = 0.0 
        self.homeGestureMovementDistance         = 0.0
        #self.currMovementDirection               = 1.0  # 0 means downward,  1 means the same note, 2 means upward

    def InitializeEnvironment ( self, scale ) : 

        Environment.InitializeEnvironment ( self, scale ) 

        self.durationChordTonesForChordLength    = 0.0 
        self.durationNonChordTonesForChordLength = 0.0 
        self.homeGestureMovementDistance         = 0.0
        #self.currMovementDirection               = 1.0  # 0 means downward,  1 means the same note, 2 means upward
        
    def printEnvironmentVariables ( self ) :        

        Environment.printEnvironmentVariables ( self ) 
        print ( "Duration of Chord Tones       : ", self.durationChordTonesForChordLength ) 
        print ( "Duration of Non Chord Tones   : ", self.durationNonChordTonesForChordLength ) 
        print ( "Home Gesture Movement Distance: ", self.homeGestureMovementDistance )
        #print ( "Movement Direction ( 0:downward, 1:same note, 2:upward) : ", self.currMovementDirection ) 
        #print ( self.durationChordTonesForChordLength , self.durationNonChordTonesForChordLength,  self.homeGestureMovementDistance )


    def updateStateParams ( self, action, homeNotePitch, data ) :         

        note     = data['notes'] 
        duration = data['duration'] 
        numNotes = len(note) 

        for i in range(numNotes) : 
            
            if ( note[i] in MusicTheory.AllChords[self.currentChord] ) :  
                self.durationChordTonesForChordLength += duration[i] 

            elif ( note[i] not in MusicTheory.AllChords[self.currentChord] ) : 
                self.durationNonChordTonesForChordLength += duration[i] 
        
        # these are holding numerical pitches, so this includes octave information
        lastNotePitch = data['pitches'][-1]
                
        self.homeGestureMovementDistance = abs ( lastNotePitch - homeNotePitch ) 

        #if ( lastNotePitch - prevNotePitch ) > 0 : 
        #    self.currMovementDirection = 2  # movement upward
        #elif ( lastNotePitch - prevNotePitch ) < 0 : 
        #    self.currMovementDirection = 0  # movement downward
        #else : 
        #    self.currMovementDirection = 1  # movement the same
            
