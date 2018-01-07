from __future__ import print_function
from RL import State
from RL import QLearning
from RL import StateAttributes
from RL import ComplexityKnobs

import sys
import math
import random
import collections

import Constants
import MidiOutput
import MusicTheory
import Environment

class Melody () : 
    '''
    '''

    def __init__ ( self, wbLevers, homeScale, homeChord, duration, melodyPL ) : 
        self.melodyPL = melodyPL 
        self.maxNoteIndex = len(melodyPL)
        self.printMelodyNotes ( self.melodyPL ) 
        
        self.desc = 'melody5' 
        self.duration  = duration
        self.homeChord = homeChord
        self.homeScale = homeScale

        self.speed = wbLevers['rhythmSpeed']

        # initialize the state attributes for the melody5 layer
        self.StateAttributes = StateAttributes.StateAttributes['melody5']
        self.numFeatures     = len( self.StateAttributes ) 
        self.features        = [ i for i in range(self.numFeatures) ]

        layerParams = None

        # initialize actions for the melody5 layer 
        self.Knobs, self.Actions, self.ReverseActions = ComplexityKnobs.setKnobs ( self.desc, wbLevers['complexity'], layerParams ) 
        self.numActions    = len(self.Actions)
        self.defaultAction = 1 #'PLAY_CHORD_TONE'


        # Create the melody5 environment
        self.env = Environment.Melody5Environment( wbLevers['tse'], wbLevers['phraseLength'], self.homeScale, self.homeChord ) 
        # Initialize the melody5 environment variables
        self.env.InitializeEnvironment ( self.homeScale ) 
        self.env.printEnvironmentVariables () 

        # Initialize the RL data Structures
        self.initializeQLearningObject ( 0 )     

        self.trainedData = collections.OrderedDict() 


    def initializeQLearningObject ( self, rlParams ) : 
        
        self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 32, 2, 0.95, 0.20, 0.95, self ) 
        self.nextState = State.State ( self.numFeatures )  # this will hold the next state object for the melody5 layer


    def printMelodyNotes ( self, melody ) : 

        for note in melody :
            print ( melody[note] ) 
        print()

    def getNextNoteToBePlayed ( self, action, previousNote, scale, chord ) : 

        #Richard's fix for not having 6 half step issues with the melody and the bass
        if ( chord  in MusicTheory.KeyDict ) : 
            scale = chord

        if ( action == 'PLAY_HOME_NOTE' ) : 
            nextNote = [ MusicTheory.AllChords[chord][0] ]

        elif ( action == 'PLAY_CHORD_TONE' ) : 
            nextNote = [ random.choice (  MusicTheory.AllChords[chord] ) ] 

        else : 

            if ( previousNote not in MusicTheory.NotesInScale[scale] ) : 
                prevNoteIndex = MusicTheory.NotesToPitch[previousNote]  
                adder = random.choice ( [1, 11] )
                while True:
                    prevNoteIndex = ( prevNoteIndex + adder ) % 12
                    previousNote  = MusicTheory.pitchToNotes[prevNoteIndex] 
                    if ( previousNote in MusicTheory.NotesInScale[scale] ) : 
                        break 


            if ( action == 'PLAY_PASSING_TONE_UP' ) : 
                nextNote = MusicTheory.PassingTones[scale][previousNote][0]

            elif ( action == 'PLAY_PASSING_TONE_DOWN' ) : 
                nextNote = MusicTheory.PassingTones[scale][previousNote][1]

            elif ( action == 'PLAY_NEIGHBOR_TONE_UP' ) : 
                nextNote = [ MusicTheory.NeighborTones[scale][previousNote][0], previousNote ]
            
            elif ( action == 'PLAY_NEIGHBOR_TONE_DOWN' ) : 
                nextNote = [ MusicTheory.NeighborTones[scale][previousNote][1], previousNote ]
                
            elif ( action == 'PLAY_CHORD_TO_CHORD_UP' ) : 
                nextNote = random.choice ( MusicTheory.ChordToneToNextChordTone[chord][scale][0] ) 

            elif ( action == 'PLAY_CHORD_TO_CHORD_DOWN' ) : 
                nextNote = random.choice ( MusicTheory.ChordToneToNextChordTone[chord][scale][1] ) 
            
        return nextNote

    def getDuration ( self, notes, remainingDuration, currNoteIndex ) : 

        numNotes = len(notes) 
        if ( numNotes == 4 ) : 
            if ( remainingDuration <= Constants.NoteDurations['0.25']['ticks'] and self.speed == 'medium' ) : # less than or equal to quarter
                del notes[2] 
                numNotes = len(notes) 
            elif ( remainingDuration <= Constants.NoteDurations['0.375']['ticks'] and self.speed == 'slow' ) : # less than or equal to three-eights
                del notes[1:2] 
                numNotes = len(notes) 


        newNotes = []
        duration = []
        velocity = [] 

        startDuration = self.melodyPL[currNoteIndex]['Clk'][0]    
        for i in range(numNotes) : 
            if ( currNoteIndex >= self.maxNoteIndex ) : 
                break
            newNotes.append ( notes[i] )
            duration.append ( self.melodyPL[currNoteIndex]['duration'] )
            velocity.append ( self.melodyPL[currNoteIndex]['velocity'] )
            endDuration = self.melodyPL[currNoteIndex]['Clk'][1]
            currNoteIndex += 1
        
           
        totalDuration = endDuration - startDuration 
        return duration, newNotes, totalDuration, velocity, currNoteIndex



    def run ( self ) :

        trainingIterations = 250
        totalActions = self.numActions - 1 # this is the total number of actions to choose from
        numExploratoryActions  = 0  # number of exploratory actions taken in this training iteration
        numExploitationActions = 0  # number of exploitation actions taken in this training iteration
        defaultActionList = [ i for i in range(self.numActions) ] 
        if ( self.speed == 'slow' ) : 
            shortenedActionList = [ 0, 1 ] 
        else : 
            shortenedActionList = [ 0, 1, 4, 5 ] 

        for trIter in range(trainingIterations) :  # called for every training iteration

            self.qLearn.initializeState() 
            self.env.InitializeEnvironment ( self.homeScale )
            self.homePitch = 0 

            chosenItems = [] 

            currentOctave = 5
            prevNote  = ''
            prevPitch = -1
            usedTicks = 0 
            remainingTicks = self.duration - usedTicks

            currentNoteIndex = 0 

            while usedTicks < self.duration :  


                if ( currentNoteIndex >= self.maxNoteIndex ) : 
                    break


                currentScale = self.melodyPL[currentNoteIndex]['scale']
                currentChord = self.melodyPL[currentNoteIndex]['chord']

                
                actionList = defaultActionList
                if ( remainingTicks  <= Constants.NoteDurations['0.125']['ticks'] ) : # less than or equal to eigth
                    actionList = shortenedActionList

                chosenData = {} 

                if ( usedTicks  == 0 ) :   # this is the first note to be played, so choose between one of the chord tones for the chord
                    typeOfAction = "Initial"
                    chosenAction = self.Actions[self.defaultAction] # PLAY_CHORD_TONE 
                    chosenNote   = self.getNextNoteToBePlayed  ( chosenAction, prevNote, currentScale, currentChord )  
                    
                    chosenDuration, chosenNote, totalDuration, velocity, currentNoteIndex = self.getDuration ( chosenNote, remainingTicks, currentNoteIndex ) 
                    
                    prevNote = chosenNote[-1]
                    prevPitch = MusicTheory.NotesToPitch[prevNote] + ( currentOctave * 12 ) 
                    self.homePitch = prevPitch
                    pitch = self.getOctavesAndPitchData ( chosenNote,  prevPitch )
                    #velocity = [ random.randint(50,80) for note in chosenNote ]
                    chosenData     = { 'action': chosenAction, 'notes':  chosenNote, 'pitches': pitch, 'chord': currentChord, 'scale': currentScale, 'duration': chosenDuration, 'totalDuration': totalDuration, 'velocity': velocity } 
                    chosenReward   = 0 
                    self.homePitch = pitch[0]
                else :                 
                    # figure out if we want to explore or exploit
                    randForExploration = random.random () 
                    exploitationThreshold = self.getRandThreshold ( trIter, trainingIterations )
                    if ( randForExploration >= exploitationThreshold ) : 
                        # epsilon greedy Exploration 
                        typeOfAction = "Explore"
                        numExploratoryActions += 1                       
                        chosenAction = self.Actions[ random.choice(actionList) ]
                        chosenNote   = self.getNextNoteToBePlayed  ( chosenAction, prevNote, currentScale, currentChord ) 
                        chosenDuration, chosenNote, totalDuration, velocity, currentNoteIndex = self.getDuration ( chosenNote, remainingTicks, currentNoteIndex ) 

                        pitch = self.getOctavesAndPitchData ( chosenNote, prevPitch )
                        #velocity = [ random.randint(50,80) for note in chosenNote ]
                        chosenData = { 'action': chosenAction, 'notes':  chosenNote, 'pitches': pitch, 'chord': currentChord, 'scale': currentScale, 'duration': chosenDuration, 'totalDuration': totalDuration, 'velocity': velocity } 

                    else :  #exploitation
                        typeOfAction = "Exploit"
                        numExploitationActions += 1
                        q       = 0.0 
                        qMax    = 0.0
                        initial = True
                        #chosenData = {} 
                        for action in actionList : 
                            currentAction   = self.Actions[action] 
                            currentNote     = self.getNextNoteToBePlayed  ( currentAction, prevNote, currentScale, currentChord ) 

                            currentDuration, currentNote, totalDuration, velocity, newCurrentNoteIndex = self.getDuration ( currentNote, remainingTicks, currentNoteIndex ) 

                            pitch = self.getOctavesAndPitchData ( currentNote, prevPitch )
                            self.getNextState ( currentAction, { 'notes': currentNote, 'duration': currentDuration, 'pitches': pitch } ) 
                            q = self.qLearn.predictQFactor ( self.nextState, self.ReverseActions[currentAction] ) 
           
                            # if ( 1 ) : 
                            #    print ( "i: ", action,  "Notes: ", currentHomeNote, "currentChord: ", currentChord, "currentScale: ", currentScale, "Duration: ", currentDuration, "Action: ", currentAction,  self.nextState.stats  )     
                            #    print ( "i: ", action,  "q:", q, "qMax: ", qMax ) 
                            
                            if ( initial or q >= qMax ) :
                                qMax    = q 
                                initial = False
                                #velocity = [ random.randint(50,80) for note in currentNote ]
                                chosenData = { 'action': currentAction, 'notes': currentNote, 'pitches': pitch, 'chord': currentChord, 'scale': currentScale, 'duration': currentDuration, 'totalDuration': totalDuration, 'velocity': velocity } 
                                chosenCurrentNoteIndex = newCurrentNoteIndex
                        # end for action in actionList 
                        currentNoteIndex = chosenCurrentNoteIndex
                    # end exploration or exploitation

                    # Assign Credit or Blame for Chosen Action
                    chosenReward = self.assignCreditOrBlameForAction ()     

                # end initial action if ( usedTicks == 0 ) 

                # UPDATE RL State after figuring out what the chosen action and notes are        
                self.qLearn.updateRL ( chosenReward,  chosenData['action'], chosenData ) 
                self.env.updateStateParams (  chosenData['action'], self.homePitch, chosenData ) 

                usedTicks += chosenData['totalDuration']
                remainingTicks = self.duration - usedTicks
                chosenItems.append ( chosenData )
                prevNote = chosenData['notes'][-1]
                prevPitch = chosenData['pitches'][-1]
                currentOctave = chosenData['pitches'][-1]//12

                if ( 0 ) :
                    print ( "Used Ticks: ", usedTicks, "remaining duration: ", remainingTicks, "Total Ticks: ", self.duration )
            # end while ( remainingTicks < self.duration ) 
            #break 
            if ( 0 ) : 
                print ( "End of iter: ", trIter, "chosenItems: ", chosenItems ) 
        # end for trIter in range( trainingIterations)
        if ( 0 ) : 
            print() 
            for item in chosenItems :
                print ( "item: ", item ) 


        self.trainedData =  self.fillGapsWithRestNotes( chosenItems )


        if ( 1 ) : 
            print() 
            for item in self.trainedData :
                print ( item ) 

        

        return ( self.trainedData ) 

    def fillGapsWithRestNotes ( self, items ) : 

        currIndex    = 0
        prevEndClk   = self.melodyPL[0]['Clk'][1]
        nextStartClk = self.melodyPL[1]['Clk'][0]

        filledGapItems = []

        for item in items : 

            newItem = { 'duration': [], 'chord': item['chord'], 'scale': item['scale'], 'action': item['action'], 'velocity': [], 'notes': [], 'pitches': [], 'totalDuration': 0 }
            
            #print ( item ) 
            for note in range(len(item['duration'])) : 

                newItem['notes'].append ( item['notes'][note])
                newItem['duration'].append ( item['duration'][note])
                newItem['velocity'].append ( item['velocity'][note])
                newItem['pitches'].append ( item['pitches'][note])


                if ( currIndex+1 >= self.maxNoteIndex ) : 
                    break 
                prevEndClk   = self.melodyPL[currIndex]['Clk'][1]
                nextStartClk = self.melodyPL[currIndex+1]['Clk'][0]


                if ( prevEndClk < nextStartClk ) : 
                    diff = nextStartClk - prevEndClk
                    newItem['notes'].append ( item['notes'][note])
                    newItem['duration'].append ( diff ) 
                    newItem['velocity'].append ( 0 ) 
                    newItem['pitches'].append ( item['pitches'][note])

                currIndex    += 1

            filledGapItems.append ( newItem ) 

        if ( 0 ) : 
            print() 
            for item in filledGapItems :
                print ( item ) 
            

        return filledGapItems

                                              




    def getOctavesAndPitchData ( self, notes, prevPitch ) : 

        pitch = [] 
        octave = prevPitch // 12

        for currNote in notes :

            currNoteIndex = MusicTheory.NotesToPitch[currNote] 
            noteA = ( octave * 12 ) + currNoteIndex            
            if ( abs(noteA - self.homePitch) > 12 ) : 
                noteA = 1000


            if ( (octave + 1) >= 8 ) : 
                noteB = 1000 
            else : 
                noteB = ( (octave+1) * 12 ) + currNoteIndex
                if ( abs(noteB - self.homePitch) > 12 ) : 
                    noteB = 1000


            if ( (octave - 1) < 4 ) : 
                noteC = 1000
            else : 
                noteC = ( (octave-1) * 12 ) + currNoteIndex 
                if ( abs(noteC - self.homePitch) > 12 ) : 
                    noteC = 1000


            diffA = abs (prevPitch - noteA ) 
            diffB = abs (prevPitch - noteB )  
            diffC = abs (prevPitch - noteC )  
            
            if ( diffA <= diffB and diffA <= diffC ) : 
                pitch.append ( noteA ) 
            elif ( diffB <= diffA and diffB <= diffC ) : 
                pitch.append ( noteB ) 
            elif ( diffC <= diffA and diffC <= diffB ) : 
                pitch.append ( noteC ) 

            prevPitch = pitch[-1] 
            octave = prevPitch // 12 

        return pitch


    def getNextState ( self, action, data ) : #data will include the note being played and duration

        note = data['notes']
        duration = data['duration']
        pitch = data['pitches'][-1]
        diffInHomePitchCurrPitch = abs ( pitch - self.homePitch )
        if ( 1 ) : 
            gestureMovement = round ( float ( (diffInHomePitchCurrPitch*1.0) / (24*1.0) ), 3 )  # why 24. we cannot go 2 octaves above homenote
            action = self.ReverseActions[action]
            #print ( "Action: ", action, "Current Pitch: ", pitch, "Home Pitch: ", self.homePitch, "Difference: ", diffInHomePitchCurrPitch, "Gesture Movement: ", gestureMovement )

        durationChordTonesForChordLength    = self.env.durationChordTonesForChordLength
        durationNonChordTonesForChordLength = self.env.durationNonChordTonesForChordLength         

        numNotes = len(note) 
        for i in range(numNotes) : 

            if ( note[i] in MusicTheory.AllChords[self.homeChord] ) :  
                durationChordTonesForChordLength += duration[i] 

            elif ( note[i] not in MusicTheory.AllChords[self.homeChord] ) : 
                durationNonChordTonesForChordLength += duration[i] 

        total = durationChordTonesForChordLength + durationNonChordTonesForChordLength
        for i in range(self.numFeatures) : 

            feat = self.features[i]

            if ( 'DURATION_CHORD_TONES_FOR_CHORD_LENGTH' in self.StateAttributes and  feat == self.StateAttributes['DURATION_CHORD_TONES_FOR_CHORD_LENGTH'] ) : 
                durationChordTones = round (float ( (durationChordTonesForChordLength*1.0) / (total*1.0) ), 3 ) 
                self.nextState.setStat ( feat, durationChordTones ) 

            elif ( 'DURATION_NON_CHORD_TONES_FOR_CHORD_LENGTH' in self.StateAttributes and  feat == self.StateAttributes['DURATION_NON_CHORD_TONES_FOR_CHORD_LENGTH'] ) : 
                durationNonChordTones = round (float ( (durationNonChordTonesForChordLength*1.0) / (total*1.0) ), 3 ) 
                self.nextState.setStat ( feat, durationNonChordTones ) 

            elif ( 'HOME_GESTURE_MOVEMENT_DISTANCE' in self.StateAttributes and  feat == self.StateAttributes['HOME_GESTURE_MOVEMENT_DISTANCE'] ) :                 
                gestureMovement = round ( float ( (diffInHomePitchCurrPitch*1.0) / (24*1.0) ), 3 )  # why 24. we cannot go 2 octaves above homenote
                self.nextState.setStat ( feat, gestureMovement ) 
          
        return self.nextState

    def getRandThreshold ( self, trIter, trainingIterations ) :
        ratioIter = round ( float ( trIter * 1.0  / trainingIterations * 1.0 ), 2 )         
        if ( ratioIter <= 0.25 ) : 
            randExploitation = 0.40 
        elif ( ratioIter > 0.25 and  ratioIter <= 0.50 ) : 
            randExploitation = 0.50 
        elif ( ratioIter > 0.50 and  ratioIter <= 0.75 ) : 
            randExploitation = 0.80 
        else :
            randExploitation = 0.90 
        if ( 0 ) : 
            print ( "trIter: ", trIter, "Num Iterations: ", trainingIterations, "Ratio: ", ratioIter , "Rand Exploitation: ", randExploitation ) 
        return randExploitation


    def assignCreditOrBlameForAction ( self ) : 
        
        durationChordTonesForChordLength    = self.env.durationChordTonesForChordLength
        durationNonChordTonesForChordLength = self.env.durationNonChordTonesForChordLength         
        total = durationChordTonesForChordLength + durationNonChordTonesForChordLength

        homeGestureMovementDistance = self.env.homeGestureMovementDistance
                
        if ( total != 0 ) : 
            ratioOfChordTones     = round ( float( (durationChordTonesForChordLength*1.0) / ( total*1.0) ), 3 ) 
            ratioOfNonChordTones  = round ( float( (durationNonChordTonesForChordLength*1.0) / ( total*1.0) ), 3 ) 
        else :
            ratioOfChordTones     = 1
            ratioOfNonChordTones  = 0


        if ( ratioOfChordTones >= self.Knobs['chordToneThresholdLow'] and ratioOfChordTones <= self.Knobs['chordToneThresholdHigh']  and 
             ratioOfNonChordTones >= self.Knobs['nonChordToneThresholdLow'] and ratioOfNonChordTones <= self.Knobs['nonChordToneThresholdHigh']  ) : 
            reward = 1.0
        else : 
            reward = -1.0

        if (  homeGestureMovementDistance <= self.Knobs['gestureMvmt'] ) : 
            reward = 1.0
        else : 
            reward = -1.0

        return reward
