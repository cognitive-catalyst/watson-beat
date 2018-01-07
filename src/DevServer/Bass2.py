from __future__ import print_function
from RL import State
from RL import QLearning
from RL import StateAttributes
from RL import ComplexityKnobs

import sys
import random
import Constants

import MidiOutput
import MusicTheory
import Environment


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


        # initialize the state attributes for the bass2 layer
        self.StateAttributes = StateAttributes.StateAttributes[self.desc]
        self.numFeatures     = len( self.StateAttributes ) 
        self.features        = [ i for i in range(self.numFeatures) ]

        isRL = False
        if isRL : 
        
            layerParams = None

            # initialize actions for the bass2 layer 
            self.Knobs, self.Actions, self.ReverseActions = ComplexityKnobs.setKnobs ( self.desc, wbLevers['complexity'], layerParams ) 
            self.numActions = len(self.Actions)
            self.defaultAction =  0 #'PLAY_HOME_NOTE'
        
            # Create the bass2 environment
            self.env = Environment.Bass2Environment( wbLevers['tse'], wbLevers['phraseLength'], scale, chord ) 
            # Initialize the bass2 environment variables
            self.env.InitializeEnvironment ( scale ) 
            # self.env.printEnvironmentVariables () 

            # Initialize the RL data Structures
            self.initializeQLearningObject ( 0 )     

            self.trainedData = [] 

        else : 
            layerParams = None
            # initialize actions for the bass2 layer 
            self.Knobs, self.Actions, self.ReverseActions = ComplexityKnobs.setKnobs ( self.desc, wbLevers['complexity'], layerParams ) 
            self.numActions = len(self.Actions)


    def initializeQLearningObject ( self, rlParams ) : 
        
        self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 32, 2, 0.95, 0.20, 0.95, self ) 
        self.nextState = State.State ( self.numFeatures )  # this will hold the next state object for the bass2 layer
        

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

    def getNextState ( self, action, data ) : #data will include the note being played and duration

        note = data['notes']
        duration = data['duration']

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
          
        return self.nextState

    def assignCreditOrBlameForAction ( self ) : 
        
        durationChordTonesForChordLength    = self.env.durationChordTonesForChordLength
        durationNonChordTonesForChordLength = self.env.durationNonChordTonesForChordLength         
        total = durationChordTonesForChordLength + durationNonChordTonesForChordLength
        
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

        return reward
    
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



    def runRL ( self ) : 
        trainingIterations = 250
        totalActions = self.numActions - 1 # this is the total number of actions to choose from
        numExploratoryActions  = 0  # number of exploratory actions taken in this training iteration
        numExploitationActions = 0  # number of exploitation actions taken in this training iteration

        for trIter in range(trainingIterations) :  # called for every training iteration

            self.qLearn.initializeState() 
            self.env.InitializeEnvironment ( self.homeScale )

            chosenItems = [] 
    
            for noteId in range(len(self.rhythm)) :

                chosenData = {} 
                chosenDuration = self.rhythm[noteId] 

                if ( noteId == 0 ) :   # this is the first note to be played, so choose between home note and the octave up
                    typeOfAction = "Initial"
                    chosenAction = random.choice ( [ 'PLAY_HOME_NOTE', 'PLAY_OCTAVE_UP' ] )
                    chosenNote, octaveUp   = self.getNextNoteToBePlayed  ( chosenAction )  
                    chosenReward = 0 
                    chosenData = { 'action': chosenAction, 'notes':  chosenNote , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [chosenDuration], 'octaveUp': octaveUp } 
                else :                 
                    # figure out if we want to explore or exploit
                    randForExploration = random.random () 
                    exploitationThreshold = self.getRandThreshold ( trIter, trainingIterations )
    
                    if ( randForExploration >= exploitationThreshold ) : 
                        # epsilon greedy Exploration 
                        typeOfAction = "Explore"
                        numExploratoryActions += 1                       
                        chosenAction           = self.Actions[ random.randint(0, totalActions) ]
                        chosenNote, octaveUp   = self.getNextNoteToBePlayed  ( chosenAction ) 
                        chosenData = { 'action': chosenAction, 'notes':  chosenNote , 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [chosenDuration], 'octaveUp': octaveUp } 
                    else :  #exploitation
                        typeOfAction = "Exploit"
                        numExploitationActions += 1
                        q       = 0.0 
                        qMax    = 0.0
                        initial = True
                        chosenData = {} 
                        for action in range(self.numActions) : 
                            currentAction   = self.Actions[action] 
                            currentDuration = self.rhythm[noteId] 
                            currentNote, octaveUp = self.getNextNoteToBePlayed  ( currentAction )
                            
                            self.getNextState ( currentAction, { 'notes': currentNote, 'duration': [currentDuration]  } ) 
                            q = self.qLearn.predictQFactor ( self.nextState, self.ReverseActions[currentAction] ) 
           
                            # if ( 1 ) : 
                            #    print ( "i: ", action,  "Notes: ", currentHomeNote, "currentChord: ", currentChord, "currentScale: ", currentScale, "Duration: ", currentDuration, "Action: ", currentAction,  self.nextState.stats  )     
                            #    print ( "i: ", action,  "q:", q, "qMax: ", qMax ) 
                            
                            if ( initial or q >= qMax ) :
                                qMax    = q 
                                initial = False
                                chosenData = { 'action': currentAction, 'notes': currentNote, 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [currentDuration], 'octaveUp': octaveUp } 
                        # end for action in range(self.numActions) : 
                    # end exploration or exploitation

                    # Assign Credit or Blame for Chosen Action
                    chosenReward = self.assignCreditOrBlameForAction () 
                # end initial action if ( noteId == 0 ) 

                # UPDATE RL State after figuring out what the chosen action and notes are        
                self.qLearn.updateRL ( chosenReward,  chosenData['action'], chosenData ) 
                self.env.updateStateParams (  chosenData['action'], chosenData ) 

                chosenItems.append ( chosenData )


            # end for noteId in range(len(self.rhythm)) :
            
        # end trIter in range(trainingIterations) :  # called for every training iteration
                


        if ( 1 ) : 
            for i in range(len(chosenItems)) : 
                print ( chosenItems[i]) 
            print() 

        iter = trainingIterations-1

        sys.exit(0) 
        return ( chosenItems ) 



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
