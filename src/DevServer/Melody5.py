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


prnFlag = True

class Melody5 ( ) : 
    '''

    '''

    def __init__ ( self, wbLevers, scale, chord, ids, duration ) :

        wbLevers['complexity'] = 'semi_complex'

        self.desc = 'melody5' 
        self.duration  = duration
        self.homeChord = chord[0]
        self.homeScale = scale[0]

        self.speed = wbLevers['rhythmSpeed']


        # store all chord ids with same duration
        self.chordIds    = ids

        # if there is more than one chord with the same duration store them here. Will be used later to fill the actions based on the first learned chord for this duration
        self.otherChords = chord
        self.otherScales = scale
        
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


        if ( prnFlag ) : 
            self.PrintClassInfo() 

        

    def initializeQLearningObject ( self, rlParams ) : 
        
        #self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 32, 2, 0.95, 0.20, 0.95, self ) 
        self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 32, 2, 0.95, 0.20, 1.0, self ) 
        self.nextState = State.State ( self.numFeatures )  # this will hold the next state object for the melody5 layer

    def PrintClassInfo ( self ) :
        print ( )
        print ( "Layer Description: ", self.desc ) 
        print ( "State Attributes: ", self.StateAttributes ) 
        print ( "Num Features: ", self.numFeatures ) 
        print ( "Features: ", self.features ) 
        
        print ( "Actions: ", self.Actions ) 
        print ( "Num Actions: ", self.numActions ) 
        print ( "Knobs: ", self.Knobs ) 
        print () 


    def getNextNoteToBePlayed ( self, action, previousNote, scale, chord ) : 

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

        self.qLearn.initializeState() 
        self.env.InitializeEnvironment ( self.homeScale )


        for trIter in range(trainingIterations) :  # called for every training iteration

            #self.qLearn.initializeState() 
            self.env.InitializeEnvironment ( self.homeScale )
            self.homePitch = 0 

            chosenItems = [] 

            currentOctave = 5
            prevNote = ''
            prevPitch = -1
            usedTicks = 0 
            remainingTicks = self.duration - usedTicks

            while usedTicks < self.duration :  
                
                actionList = defaultActionList
                if ( remainingTicks  <= Constants.NoteDurations['0.125']['ticks'] ) : # less than or equal to eigth
                    actionList = shortenedActionList

                chosenData = {} 

                if ( usedTicks  == 0 ) :   # this is the first note to be played, so choose between one of the chord tones for the chord
                    typeOfAction = "Initial"
                    chosenAction = self.Actions[self.defaultAction] # PLAY_CHORD_TONE 
                    chosenNote   = self.getNextNoteToBePlayed  ( chosenAction, prevNote, self.homeScale, self.homeChord)  
                    chosenDuration, chosenNote, totalDuration = self.getDuration ( chosenNote, remainingTicks ) 
                    prevNote = chosenNote[-1]
                    prevPitch = MusicTheory.NotesToPitch[prevNote] + ( currentOctave * 12 ) 
                    self.homePitch = prevPitch
                    pitch = self.getOctavesAndPitchData ( chosenNote,  prevPitch )
                    velocity = [ random.randint(50,80) for note in chosenNote ]
                    chosenData     = { 'action': chosenAction, 'notes':  chosenNote, 'pitches': pitch, 'chord': self.homeChord, 'scale': self.homeScale, 'duration': chosenDuration, 'totalDuration': totalDuration, 'velocity': velocity } 
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
                        chosenNote   = self.getNextNoteToBePlayed  ( chosenAction, prevNote, self.homeScale, self.homeChord ) 
                        chosenDuration, chosenNote, totalDuration = self.getDuration ( chosenNote, remainingTicks ) 
                        pitch = self.getOctavesAndPitchData ( chosenNote, prevPitch )
                        velocity = [ random.randint(50,80) for note in chosenNote ]
                        chosenData = { 'action': chosenAction, 'notes':  chosenNote, 'pitches': pitch, 'chord': self.homeChord, 'scale': self.homeScale, 'duration': chosenDuration, 'totalDuration': totalDuration, 'velocity': velocity } 

                    else :  #exploitation
                        typeOfAction = "Exploit"
                        numExploitationActions += 1
                        q       = 0.0 
                        qMax    = 0.0
                        initial = True
                        #chosenData = {} 
                        for action in actionList : 
                            currentAction   = self.Actions[action] 
                            currentNote     = self.getNextNoteToBePlayed  ( currentAction, prevNote, self.homeScale, self.homeChord ) 
                            currentDuration, currentNote, totalDuration = self.getDuration ( currentNote, remainingTicks )
                            pitch = self.getOctavesAndPitchData ( currentNote, prevPitch )
                            self.getNextState ( currentAction, { 'notes': currentNote, 'duration': currentDuration, 'pitches': pitch } ) 
                            q = self.qLearn.predictQFactor ( self.nextState, self.ReverseActions[currentAction] ) 
           
                            # if ( 1 ) : 
                            #    print ( "i: ", action,  "Notes: ", currentHomeNote, "currentChord: ", currentChord, "currentScale: ", currentScale, "Duration: ", currentDuration, "Action: ", currentAction,  self.nextState.stats  )     
                            #    print ( "i: ", action,  "q:", q, "qMax: ", qMax ) 
                            
                            if ( initial or q >= qMax ) :
                                qMax    = q 
                                initial = False
                                velocity = [ random.randint(50,80) for note in currentNote ]
                                chosenData = { 'action': currentAction, 'notes': currentNote, 'pitches': pitch, 'chord': self.homeChord, 'scale': self.homeScale, 'duration': currentDuration, 'totalDuration': totalDuration, 'velocity': velocity } 
                        # end for action in actionList 
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
            if ( 1 ) : 
                #print ( "Iteration Number: " , trIter,  self.env.durationChordTonesForChordLength , self.env.durationNonChordTonesForChordLength,  self.env.homeGestureMovementDistance )
                print ( self.env.durationChordTonesForChordLength , self.env.durationNonChordTonesForChordLength,  self.env.homeGestureMovementDistance )

        # end for trIter in range( trainingIterations)


        if ( 1 ) : 
            for i in range(len(chosenItems)) : 
                print ( "Item: ",  chosenItems[i]) 
            print() 

        self.AssignRestNotes ( chosenItems ) 
        self.populateAdditionalChordsOfSameDuration ( chosenItems ) 
        

        return ( self.trainedData ) 


    def getRandThreshold ( self, trIter, trainingIterations ) :
        ratioIter = round ( float ( trIter * 1.0  / trainingIterations * 1.0 ), 2 )         
        if ( ratioIter <= 0.25 ) : 
            randExploitation = 0.40 
        elif ( ratioIter > 0.25 and  ratioIter <= 0.50 ) : 
            randExploitation = 0.50 
        elif ( ratioIter > 0.50 and  ratioIter <= 0.75 ) : 
            randExploitation = 0.95 
        else :
            randExploitation = 0.99 
        if ( 0 ) : 
            print ( "trIter: ", trIter, "Num Iterations: ", trainingIterations, "Ratio: ", ratioIter , "Rand Exploitation: ", randExploitation ) 
        return randExploitation


    def getDuration ( self, notes, remainingDuration ) : 
        numNotes = len(notes) 

        if ( numNotes == 4 ) : 
            if ( remainingDuration <= Constants.NoteDurations['0.25']['ticks'] and self.speed == 'medium' ) : # less than or equal to quarter
                del notes[2] 
                numNotes = len(notes) 
            elif ( remainingDuration <= Constants.NoteDurations['0.375']['ticks'] and self.speed == 'slow' ) : # less than or equal to three-eights
                del notes[1:2] 
                numNotes = len(notes) 
                
            #else : 
            #    print ( "Notes: ", notes ) 

        while ( True ) : 
            noteLength    = random.choice ( Constants.DurationBreakdown[self.speed]['DurationProbsForNotes'][numNotes] ) 
            totalDuration = Constants.DurationBreakdown[self.speed][numNotes][noteLength]['total'] 
            if ( totalDuration <= remainingDuration ) : 
                break 
            #print ( "Stuck: ", "Note Length: ", noteLength, "notes: ", notes, "numNotes: ", numNotes, "remainingDuration: ", remainingDuration, "duration: ", totalDuration ) 
            

        duration = random.choice ( Constants.DurationBreakdown[self.speed][numNotes][noteLength]['choices'] ) 

        if ( len(duration) == len(notes) ) :            
            return  duration, notes, totalDuration

        diffInNotes = len(duration) - 2
        newNotes = [ notes[0] ] 
        for i in range ( diffInNotes ) : 
            newNotes.append( random.choice( notes ) )
            #print ( "i: ",  i, "diffInNotes: ", diffInNotes, "newNotes: ", newNotes, "notes: ", notes, "duration: ", duration, "total Duration: " , totalDuration, "noteLength: ", noteLength ) 
        if ( diffInNotes >= 0 ) :
            newNotes.append( notes[-1])

        # sanity check . FIX ME. remove this check for speed
        if ( len(newNotes) != len(duration) ) : 
            print()
            print ( "Notes and Durations do not match" ) 
            print ( "Notes: ", newNotes, len(newNotes) ) 
            print ( "Duration: ", duration, len(duration) )
            print ( "Abort\n" ) 
            sys.exit(0) 

        # assign pitch information for new notes      
        return  duration, newNotes, totalDuration

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

    def populateAdditionalChordsOfSameDuration ( self, items ) : 

        numChords = len(self.otherScales ) 
        self.trainedData[self.chordIds[0]] = items


        #print ( "Last Note: ", items[-1] ) 
        #sys.exit(0) 

        prevPitch = items[-1]['pitches'][-1]  
        prevOctave = prevPitch // 12
        prevNote = items[-1]['notes'][-1]  
        for id in range ( 1, numChords, 1 ) : 

            #prevNote = ''
            scale    = self.otherScales[id]
            chord    = self.otherChords[id]
            chordId  = self.chordIds[id]
            newItems = [] 

            if ( 1 )  :
                print ( "Scale: ", scale, "Chord: ", chord, "Prev Note: ", prevNote ) 
            for item in items : 
                action    = item['action'] 
                notes     = item['notes'] 
                duration  = item['duration']
                velocity  = item['velocity']
                nextNotes = self.getNextNoteToBePlayed ( action, prevNote, scale , chord )
                if ( 1 )  :
                    print ( "Action: ", action, "Notes: ", notes, "New Notes for chord: ", nextNotes  ) 

                diffInNotes = len(duration) - 2   # why 2, because we will copy the first and last note according to the appropriate action. the rest will be filled out based on the original rhythm learned
                # For example if notes = [  B A A G ] and new scale is AMinor and prev note is G, then nextNotes will be [ F E D ], and then after the for loop including the diff notes, it can be [ F E E D ] or [ F F E D ] etc.

                newNotes = [ nextNotes[0] ] 
                for i in range ( diffInNotes ) : 
                    newNotes.append( random.choice( nextNotes ) )
                    #print ( i, diffInNotes, newNotes) 
                if ( diffInNotes >= 0 ) :
                    newNotes.append( nextNotes[-1])
                    
                pitch = self.getOctavesAndPitchData ( newNotes,  prevPitch )
                print ( "Current Pitch: ", pitch, "Current Notes: ", newNotes, "prevNotes: ", prevNote, "prev Pitches: ", prevPitch, "prev Octave: ", prevOctave  ) 


                #pitch = [] 
                if ( 1 )  :
                    print ( "Action: ", action, "Notes: ", notes, "New Notes for chord: ", newNotes  ) 
                    print() 


                newItem  = { 'action': action, 'notes':  newNotes, 'pitches': pitch, 'chord': chord, 'scale': scale, 'duration': duration, 'velocity': velocity } 
                newItems.append ( newItem ) 

                prevNote = newNotes[-1]
                prevPitch = pitch[-1]
                prevOctave = prevPitch // 12


                if ( 1 )  :
                    print ( "Scale: ", scale, "Chord: ", chord, "Prev Note: ", prevNote ) 

            self.trainedData[chordId] = newItems


        if ( 1 ) : 
            for chId in self.trainedData : 
                print ( "Chord Id: ", chId ) 
                for item in self.trainedData[chId] : 
                    print ( item ) 
                print()
                

        
       # sys.exit(0) 

        
    def AssignRestNotes ( self, chosenItems )  :

        if ( 1 ) : 
            for i in range(len(chosenItems)) : 
                print ( "Item: ",  chosenItems[i]) 
            print() 

        restNoteProbability = random.randint ( 0, 100 ) 

        restNoteProbability = 35
        restNoteProbability = 75
        restNoteProbability = 15
        restNoteProbability = 15

        if ( restNoteProbability < 30 ) : 
            restNoteDuration = self.duration * 0.10
        elif ( restNoteProbability < 60 ) : 
            restNoteDuration = self.duration * 0.25
        else :
            restNoteDuration = self.duration * 0.50

        if ( 1 ) : 
            print ( "Before Rest Note Duration: ", restNoteDuration, "Probability: ", restNoteProbability, "Total Duration: ", self.duration ) 

        if ( restNoteDuration % Constants.NoteDurations['0.125']['ticks'] != 0 ) : 
            div = int ( math.ceil ( restNoteDuration / Constants.NoteDurations['0.125']['ticks'] ) )
            restNoteDuration = div * Constants.NoteDurations['0.125']['ticks']
            if ( restNoteDuration == 0 ) : 
                restNoteDuration = Constants.NoteDurations['0.125']['ticks']


        if ( 1 ) :
            print ( "After  Rest Note Duration: ", restNoteDuration, "Probability: ", restNoteProbability, "Total Duration: ", self.duration ) 

        durationLeft = restNoteDuration 
        while ( durationLeft > 0 ) :
            # pick item to replace notes with rest notes
            pickRandItem1 = random.randint ( 0, len(chosenItems)-1 ) 
            if ( 1 ) : 
                print ( "Pick Random Item: ", pickRandItem1 ) 

            # pick note within item to replace with rest notes
            numNotesInItem = len(chosenItems[pickRandItem1]['notes']) 
            pickRandItem2 = random.randint ( 0, numNotesInItem-1 ) 
            if ( 1 ) : 
                print ( "Pick note in Random Item: ", pickRandItem2 ) 
            # if it is already a rest note, pick another item and sub item
            if ( chosenItems[pickRandItem1]['velocity'][pickRandItem2] == 0 ) : 
                continue

            print ( "Here", chosenItems[pickRandItem1]['notes'], chosenItems[pickRandItem1]['notes'][pickRandItem2], chosenItems[pickRandItem1]['velocity'], chosenItems[pickRandItem1]['velocity'][pickRandItem2] )   

            # if duration of chosen note within item is less than the rest duration that is left, then make this note a rest note and continue
            if ( chosenItems[pickRandItem1]['duration'][pickRandItem2] <= durationLeft ) : 
                chosenItems[pickRandItem1]['velocity'][pickRandItem2] = 0
                durationLeft -= chosenItems[pickRandItem1]['duration'][pickRandItem2]
                print (  "Note: ", chosenItems[pickRandItem1]['notes'][pickRandItem2], "duration Left: ", durationLeft, chosenItems[pickRandItem1]['notes'][pickRandItem2] ) 
                print ( chosenItems[pickRandItem1]['notes'], chosenItems[pickRandItem1]['duration'], "velocity:", chosenItems[pickRandItem1]['velocity'] ) 
                print() 
                continue
            

            print ( "Here 1" ) 

            newNotes = []
            newDuration = [] 
            newVelocity = [] 
            newPitches = [] 
            for i in range(pickRandItem2) : 
                newNotes.append ( chosenItems[pickRandItem1]['notes'][i] ) 
                newDuration.append ( chosenItems[pickRandItem1]['duration'][i] ) 
                newVelocity.append ( chosenItems[pickRandItem1]['velocity'][i] ) 
                newPitches.append ( chosenItems[pickRandItem1]['pitches'][i] ) 
                
            print ( "Here 2: ", newNotes, newDuration, newVelocity ) 

            if ( random.randint ( 0 , 100 ) > 50 ) :
                newNotes.append ( chosenItems[pickRandItem1]['notes'][pickRandItem2] ) 
                newPitches.append ( chosenItems[pickRandItem1]['pitches'][pickRandItem2] )                 
                newDuration.append ( durationLeft ) 
                newVelocity.append ( 0 ) 
                newNotes.append ( chosenItems[pickRandItem1]['notes'][pickRandItem2] ) 
                newDuration.append ( chosenItems[pickRandItem1]['duration'][pickRandItem2] - durationLeft ) 
                newVelocity.append ( chosenItems[pickRandItem1]['velocity'][pickRandItem2] )                 
                newPitches.append ( chosenItems[pickRandItem1]['pitches'][pickRandItem2] )                 

                print ( "Here 3a: ", newNotes, newDuration, newVelocity ) 

            else : 
                newNotes.append ( chosenItems[pickRandItem1]['notes'][pickRandItem2] ) 
                newDuration.append ( chosenItems[pickRandItem1]['duration'][pickRandItem2] - durationLeft ) 
                newVelocity.append ( chosenItems[pickRandItem1]['velocity'][pickRandItem2] )                 
                newPitches.append ( chosenItems[pickRandItem1]['pitches'][pickRandItem2] )                 
                newNotes.append ( chosenItems[pickRandItem1]['notes'][pickRandItem2] ) 
                newPitches.append ( chosenItems[pickRandItem1]['pitches'][pickRandItem2] )                 
                newDuration.append ( durationLeft ) 
                newVelocity.append ( 0 ) 


                print ( "Here 3b: ", newNotes, newDuration, newVelocity ) 
                
            for i in range ( pickRandItem2+1, numNotesInItem, 1 ) :
                newNotes.append ( chosenItems[pickRandItem1]['notes'][i] ) 
                newDuration.append ( chosenItems[pickRandItem1]['duration'][i] ) 
                newVelocity.append ( chosenItems[pickRandItem1]['velocity'][i] ) 
                newPitches.append ( chosenItems[pickRandItem1]['pitches'][i] )                 

            print ( "Here 4: ", newNotes, newDuration ) 
            chosenItems[pickRandItem1]['notes'] = newNotes
            chosenItems[pickRandItem1]['duration'] = newDuration
            chosenItems[pickRandItem1]['velocity'] = newVelocity
            chosenItems[pickRandItem1]['pitches'] = newPitches
            
            durationLeft = 0 
            print ( "Duration Left: ", durationLeft ) 
            print() 

        if ( 1 ) : 
            for i in range(len(chosenItems)) : 
                print ( "Item: ",  chosenItems[i]) 
            print() 

            

