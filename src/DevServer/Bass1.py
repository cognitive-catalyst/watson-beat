from __future__ import print_function
from RL import State
from RL import QLearning
from RL import StateAttributes
from RL import ComplexityKnobs

import sys
import random


import Constants
import collections
import MusicTheory
import Environment


prnFlag = True

class Bass1 ( ) : 
    '''

    '''

    def __init__ ( self, wbLevers ) :

        self.desc = 'bass1' 
        self.tse  = Constants.TSEs[wbLevers['tse']]
        self.primaryScale = wbLevers['primaryScale']
        self.id = wbLevers['id']
        self.mood = wbLevers['mood'] 
        self.complexity = wbLevers['complexity']

        # initialize the state attributes for the bass1 layer
        self.StateAttributes = StateAttributes.StateAttributes['bass1']
        self.numFeatures     = len( self.StateAttributes ) 
        self.features        = [ i for i in range(self.numFeatures) ]

        self.trueMinPenalty = 4 # ( 4 + 0 + 0 ) 
        self.trueMaxPenalty = -24   # ( 0 + ( -5 ) + ( -19 ) ) 

        self.penaltyBase = ( self.trueMaxPenalty * -1 ) + 1  # why 25, beacuse the adder for making all penalties positive is 25. why 25, because the maximum penalty is -24 and the min penalty = 4 
        self.penaltyMin  = self.penaltyBase + self.trueMinPenalty # so min penalty after adder = 4+25 = 29
        self.penaltyMax  = self.penaltyBase + self.trueMaxPenalty # so max penalty after adder = -24 + 25 = 1

        self.trueMinPenalty = 7 
        self.trueMaxPenalty = -19 

        self.penaltyBase = ( self.trueMaxPenalty * -1 ) + 1  # why 20, beacuse the adder for making all penalties positive is 20. why 20, because the maximum penalty is -19 and the min penalty = 7 
        self.penaltyMin  = self.penaltyBase + self.trueMinPenalty # so min penalty after adder = 7+20 = 27
        self.penaltyMax  = self.penaltyBase + self.trueMaxPenalty # so max penalty after adder = -19 + 20 = 1


        self.trueMinPenalty = 7 
        self.trueMaxPenalty = -30

        self.penaltyBase = ( self.trueMaxPenalty * -1 ) + 1  
        self.penaltyMin  = self.penaltyBase + self.trueMinPenalty
        self.penaltyMax  = self.penaltyBase + self.trueMaxPenalty 



        
        layerParams = { 'minPenalty': self.penaltyMin, 'maxPenalty': self.penaltyMax }

        # initialize actions for the bass1 layer 
        self.Knobs, self.Actions, self.ReverseActions = ComplexityKnobs.setKnobs ( 'bass1', wbLevers['complexity'], layerParams ) 
        self.numActions = len(self.Actions)
        self.defaultAction =  3 #'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY'
        
        # Create the bass1 environment        
        self.env = Environment.Bass1Environment( wbLevers['tse'], wbLevers['phraseLength'], wbLevers['primaryScale'], wbLevers['mood'] ) 
        # Initialize the bass1 environment variables
        self.env.InitializeEnvironment ( wbLevers['primaryScale'] ) 
        #self.env.printEnvironmentVariables () 

        # Initialize the RL data Structures
        self.initializeQLearningObject ( 0 )     

        self.trainedData = [] 



    def initializeQLearningObject ( self, rlParams ) : 
        
        #self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 32, 2, 0.95, 0.20, 0.95, self ) 
        #self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 32, 2, 0.95, 0.20, 1.0, self ) 
        self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 16, 2, 0.95, 0.10, 1.0, self ) 
        #self.qLearn    = QLearning.QLearning ( self.numFeatures, self.features, self.numActions, 1024, 0.50, 16, 2, 0.95, 0.10, 0.95, self ) 
        self.nextState = State.State ( self.numFeatures )  # this will hold the next state object for the bass1 layer
        

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

        
    
    def assignCreditOrBlameForAction ( self, chosenAction, data ) : # data holds the chord and the scale 

        penalty = data['penalty']

        if ( self.complexity == 'super_simple' ) : 
            if ( chosenAction == 'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY' ) : 
                reward = -1.0 
                return reward
            elif ( chosenAction == 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP' ) : 
                reward = 2.0
                return reward
            elif ( chosenAction == 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' ) : 
                reward = 1.0
                return reward
            elif ( chosenAction == 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' ) : 
                reward = -3.0 
                return reward

            
        

        if ( 0 ) : 
            print ( "................................................................" ) 
            print ( "Start Assign Credit Or Blame for chosen Action: ", chosenAction ) 

        if ( penalty >= self.Knobs['cprogJumpLow'] and penalty <= self.Knobs['cprogJumpHigh'] ) :
            reward = 2.0
        else :
            reward = -2.0

        if ( 0 ) : 
            print ( "Penalty: ", penalty, "cprogjumplow: ", self.Knobs['cprogJumpLow'], "cprogjumphigh: ", self.Knobs['cprogJumpHigh'], "Immediate Reward: ", reward ) 
        
        if ( 0 ) : 
            print ( "Immediate Reward: ", reward ) 
            print ( "End Assign Credit Or Blame for chosen Action: ", chosenAction ) 
            print ( ".............................................................." ) 
        return reward
        

    def getNextState ( self, action, data ) : #data will include the following: chord, scale, 

        penalty = data['penalty']

        getNextStatePrintFlag = True
        getNextStatePrintFlag = False

        #homeChordMovementDistance = round ( ( float ( 1.0 / ( penalty * 1.0 ) ) ), 3 )  
        #self.nextState.setStat ( 0, homeChordMovementDistance ) 

        homeChordMovementDistance = round ( ( float ( ( penalty * 1.0 ) / ( self.penaltyMin+1 * 1.0 ) ) ), 3 )  
        if ( homeChordMovementDistance > 1 ) : 
            print ( "homeChordMovementDistance : ", homeChordMovementDistance, "Penalty: ", penalty, "penalty min: ", self.penaltyMin ) 
            print ( "State value greater than 1.0. Abort\n" ) 
            sys.exit(0) 
        self.nextState.setStat ( 0, homeChordMovementDistance ) 



        #numCommonNotesToPreviousChord = round ( float ( ( MusicTheory.ChordSimilarity[currentChord][chord] * 1.0) / ( 5.0 ) ), 3 )
        #numCommonNotesToHomeChord     = round ( float ( ( MusicTheory.ChordSimilarity[homeChord][chord] * 1.0 ) / ( 5.0 ) ), 3 )
        #numCommonNotesToPrimaryScale  = round ( float ( ( len ( list(set(notesInHomeScale).intersection(notesInCurrScale))) * 1.0 )/ ( 12.0 ) ), 3 )


        #numCommonNotesToHomeChord     = MusicTheory.ChordSimilarity[homeChord][chord]
        #numCommonNotesToPrimaryScale  = len(list(set(notesInHomeScale).intersection(notesInCurrScale))) 
        #homeChordMovementDistance     = round ( float ( (( numCommonNotesToHomeChord + numCommonNotesToPrimaryScale ) * 1.0 ) / ( 12.0 + 5.0 ) ), 3 ) 



        if ( getNextStatePrintFlag ) :            

            chord   = data['chord']
            scale   = data['scale']
            primaryScale  = self.env.primaryScale
            homeChord     = self.env.homeChord
            
            currentChord = self.env.currentChord
            print() 
            print ( "Action: ", action ) 
            print ( "Current Scale   : ", scale ) 
            print ( "Primary Scale   : ", primaryScale ) 
            print ( "Home Chord      : ", homeChord ) 
            print ( "Previous Chord  : ", currentChord ) 
            print ( "Next     Chord  : ", chord ) 

            #print ( "Num Common Notes To Previous Chord: ", numCommonNotesToPreviousChord*5 ) 
            #print ( "Num Common Notes To Home Chord    : ", numCommonNotesToHomeChord ) 
            #print ( "Num Common Notes To Primary Scale : ", numCommonNotesToPrimaryScale ) 
            print ( "Curr Penalty: ", penalty ) 
            print ( "Home Chord Movement Distance      : ", homeChordMovementDistance ) 
            print() 
        #feat = self.features[0]
        #if ( 'HOME_CHORD_MOVEMENT_DISTANCE' in self.StateAttributes and  feat == self.StateAttributes['HOME_CHORD_MOVEMENT_DISTANCE'] ) : 
        
 
        return self.nextState


# BEGIN Helper Functions 
    def getRandThreshold ( self, trIter, trainingIterations ) :
        ratioIter = round ( float ( trIter * 1.0  / trainingIterations * 1.0 ), 2 )         

        if ( trIter == trainingIterations-1 ) : 
            randExploitation = 1.0 
            return randExploitation

        if ( ratioIter <= 0.25 ) : 
            randExploitation = 0.40    # which implies explore 60% of the time during the first 25% of the iterations
        elif ( ratioIter > 0.25 and  ratioIter <= 0.50 ) : 
            randExploitation = 0.70    # which implies explore 50% of the time between 25% to 50% of the iterations
        elif ( ratioIter > 0.50 and  ratioIter <= 0.75 ) : 
            randExploitation = 0.95 
        else :
            randExploitation = 0.97 
        if ( 0 ) : 
            print ( "trIter: ", trIter, "Num Iterations: ", trainingIterations, "Ratio: ", ratioIter , "Rand Exploitation: ", randExploitation ) 
        return randExploitation

    def getInitialChordForScale ( self, scale ) : 
        homeNote = MusicTheory.FirstMeasureNotes[scale][0]
        homeChord = scale 
        if ( 0 ) : 
            penalty = self.penaltyMin 
            print ( "Next Chord: ", homeChord, "Next Scale: ", scale, 'homeNote: ', homeNote  ) 


        penalty = self.env.cpJumps.ChordProgressions[homeChord]['obvious']['PLAY_CHORD_PROGRESSION_TONE_SML_JUMP'][homeChord][5]

        return homeNote, homeChord, scale, penalty

    def getCPJump ( self, action ) :

        numScalesSeen = len( self.scalesInUse ) 
        
        currChord    = self.env.currentChord
        currScale    = self.env.currentScale
        homeScale    = self.env.primaryScale
        homeChord    = self.env.homeChord
        cpComplexity = random.choice ( self.Knobs['CProgComplexity'] )  # choose one between obvious, unusual, and obscure

        if ( 0 ) : 
            print() 
            print ( "Home Scale: ", homeScale, "Current Chord: ", currChord, "cpComplexity: ", cpComplexity, "Action: ", action ) 

        allTuples =  self.env.cpJumps.ChordProgressions[currChord][cpComplexity][action] 
        if ( 0 ) : 
            print ( "Action: ", action, "allTuples: ", allTuples ) 

        if ( len(allTuples) == 0 ) : 
            nextChord    = self.env.currentChord
            nextScale    = self.env.currentScale
            nextHomeNote = MusicTheory.AllChords[nextChord][0] 
            penalty = self.penaltyMin 
        else : 

            for i in range(10) : # try for 10 times to get a chord that fits into the max number of scales. if not use previous chord as the option

                nextChord  = random.choice ( allTuples.keys() ) 
                nextScale  = self.env.cpJumps.ChordProgressions[currChord][cpComplexity][action][nextChord][1] 

                if ( 0 ) :
                    print ( "Next Chord: ", nextChord ) 
                    print ( "Next Scale: ", nextScale ) 
                
                break 
            
                if ( 0 ) :
                    print ( "i: ", i, "Home Scale: ", homeScale, "Current Chord: ", currChord, "cpComplexity: ", cpComplexity, "Action: ", action ) 
                    print ( "No Scale yet", "NextChord: ", nextChord, "Next Scale: ",nextScale ) 

            if ( i == 10 ) :
                nextChord    = self.env.currentChord
                nextScale    = self.env.currentScale

            nextHomeNote = MusicTheory.AllChords[nextChord][0] 
            penalty = self.env.cpJumps.ChordProgressions[currChord][cpComplexity][action][nextChord][5] + self.penaltyBase 
            if ( penalty < 1 ) :  # sanity check
                print ( "Penalty is less than 1. That can never happen. Need to increase adder" ) ;
                print ( "Abort" ) 
                print ( "Next Chord: ", nextChord, "Next Scale: ", nextScale, 'homeNote: ', nextHomeNote, "Penalty: ", penalty  ) 
                print() 
                sys.exit(0) 

        if ( 0 ) : 
            print ( "Next Chord: ", nextChord, "Next Scale: ", nextScale, 'homeNote: ', nextHomeNote, "Penalty: ", penalty  ) 
            print() 


        return nextHomeNote, nextChord, nextScale, penalty

    def getNextChordToBePlayed ( self, action ) : 
    
        if ( action == 'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY' ) : 
            return self.getInitialChordForScale ( self.env.primaryScale )
        else: 
            return self.getCPJump ( action ) 
# END Helper Functions

    def run ( self, CPTicks ) :   # CPTicks stores the chord durations for each chord

        trainingIterations = 500
        trainingIterations = 200
        totalActions = self.numActions - 1 # this is the total number of actions to choose from
        numExploratoryActions  = 0  # number of exploratory actions taken in this training iteration
        numExploitationActions = 0  # number of exploitation actions taken in this training iteration
        numInitialActions = 0 

        self.qLearn.initializeState() 
        self.env.InitializeEnvironment ( self.primaryScale )

        for trIter in range(trainingIterations) :  # called for every training iteration

            #self.qLearn.initializeState() 
            #self.env.InitializeEnvironment ( self.primaryScale )

            cpIndex = 0  # this is the chord progression index
            chosenItems = [] 
            self.scalesInUse = {}

            if ( 0 ) : 
                print( "--------------------------------------------------------------------------------" ) 
                print ( "Iteration Num: ", trIter ) 

            rewardForIteration = 0 
            for cpIndex in range(len(CPTicks) )  :  # called everytime you want to perform an action
                
                
                chosenData = {} 
                chosenDuration = CPTicks[cpIndex]                
                if ( 0 ) : 
                    print() 

                if ( cpIndex == 0 ) :  # this is the first chord to be played, so choose 'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY'
                    typeOfAction = "Initial"
                    chosenAction = 'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY'
                    chosenHomeNote, chosenChord, chosenScale, penalty = self.getInitialChordForScale ( self.primaryScale )                     
                    chosenReward = 0 
                    numInitialActions += 1
                    chosenData = { 'action': chosenAction, 'notes': [chosenHomeNote], 'chord': chosenChord, 'scale': chosenScale, 'duration': [chosenDuration], 'penalty': penalty } 
                    self.scalesInUse[chosenScale] = True                    
                    if ( 0 ) : 
                        print ( "Chord: ", cpIndex+1 , "Action type: ", typeOfAction, "Action: ", chosenAction, chosenChord ) 
                    rewardForIteration += chosenReward
                    #print ( "Chord Id: ", cpIndex, "Chosen Reward: ", chosenReward, "Chosen Action: ", chosenData['action'], "type: ", typeOfAction ) 

                else : 
                    # figure out if we want to explore or exploit
                    randForExploration = random.random ()              
                    exploitationThreshold = self.getRandThreshold ( trIter, trainingIterations )
                    if ( 0 ) : 
                        ratioIter = round ( float ( trIter * 1.0  / trainingIterations * 1.0 ), 2 )         
                        print ( "trIter: ", trIter, "Num Iterations: ", trainingIterations, "Ratio: ", ratioIter , "Rand Exploitation: ", exploitationThreshold, "Rand Exploration: ", randForExploration ) 

                    if ( randForExploration >= exploitationThreshold ) : 
                        # epsilon greedy Exploration 
                        typeOfAction = "Explore"
                        numExploratoryActions += 1                       
                        chosenAction = self.Actions[ random.randint(0, totalActions) ]
                        chosenAction = self.Actions[ random.randint(0, totalActions-1) ]
                        chosenHomeNote, chosenChord, chosenScale, penalty = self.getNextChordToBePlayed  ( chosenAction ) 
                        chosenData = { 'action': chosenAction, 'notes': [ chosenHomeNote ], 'chord': chosenChord, 'scale': chosenScale, 'duration': [chosenDuration], 'penalty': penalty } 
                        if ( 0 ) : 
                            print ( "Chord: ", cpIndex+1 , "Action type: ", typeOfAction, "Action: ", chosenAction, chosenChord ) 


                    else :  #exploitation
                        typeOfAction = "Exploit"
                        numExploitationActions += 1
                        q       = 0.0 
                        qMax    = 0.0
                        initial = True
                        chosenData = {} 
                        for action in range(self.numActions) : 
                            if ( action == self.numActions-1 ) : #'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY' ) : 
                                continue 
                            currentAction   = self.Actions[action] 
                            currentDuration = CPTicks[cpIndex]
                            currentHomeNote, currentChord, currentScale, penalty = self.getNextChordToBePlayed  ( currentAction )

                            self.getNextState ( currentAction, { 'chord': currentChord, 'scale': currentScale, 'penalty': penalty } ) 
                            q = self.qLearn.predictQFactor ( self.nextState, self.ReverseActions[currentAction] ) 
       
                            if ( 0 ) : 
                                print ( "Chord: ", cpIndex+1 , "Action type: ", typeOfAction, "Action: ", currentAction, currentChord ) 
                                print ( "i: ", action,  "Notes: ", currentHomeNote, "currentChord: ", currentChord, "currentScale: ", currentScale, "Duration: ", currentDuration, "Action: ", currentAction,  "Next State: ", self.nextState.stats, "penalty: ", penalty  )     
                                print ( "i: ", action,  "q:", q, "qMax: ", qMax ) 

                            if ( initial or q >= qMax ) :
                                qMax    = q 
                                initial = False                                
                                chosenData = { 'action': currentAction, 'notes': [currentHomeNote], 'chord': currentChord, 'scale': currentScale, 'duration': [currentDuration],  'penalty': penalty } 
                        #end for action in range(self.numActions):
                        if ( 0 ) : 
                            print ( "Chord: ", cpIndex+1 , "Action type: ", typeOfAction, "Action: ", chosenData['action'], chosenData['chord'] ) 

                    #end exploration or exploitation
                                
                    # Assign Credit or Blame for Chosen Action
                    chosenReward = self.assignCreditOrBlameForAction (  chosenData['action'], chosenData ) 
                    #print ( "Chord Id: ", cpIndex, "Chosen Reward: ", chosenReward, "Chosen Action: ", chosenData['action'], "type: ", typeOfAction ) 
                    self.scalesInUse[chosenData['scale']] = True                    
                    rewardForIteration += chosenReward
                # end initial action  if ( cpIndex == 0 ) 
        

                # UPDATE RL State after figuring out what the chosen action and notes are        
                self.qLearn.updateRL ( chosenReward, chosenData['action'], chosenData ) 
                self.env.updateStateParams ( chosenData['action'], chosenData ) 

                chosenItems.append ( chosenData )
            # End for cpIndex in range(len(CPTicks) )  :

            #print ( rewardForIteration ) 
            #print ( "Iteration Number: ", trIter, "Total Reward: ", rewardForIteration ) 

            #Add chosen items of this training session to trained data
            self.trainedData.append ( chosenItems ) 

        #End for loop trIter

        if ( 0 ) : 
            for i in range(len(chosenItems)) : 
                print ( "Chosen Item: ", chosenItems[i]) 
            if ( 0 ) : 
                print ( "Num Exploratory : ", numExploratoryActions ) 
                print ( "Num Exploitation: ", numExploitationActions ) 
                print ( "Num Initial Actions: ", numInitialActions ) 

        iter = trainingIterations-1
        
        self.Chords = collections.OrderedDict()  # collection of Phrases
        self.Chords[0] = collections.OrderedDict()  # collection of chords within phrase
        for chId in range(len(self.trainedData[iter])) : 
            self.Chords[0][chId] = [] 
            self.Chords[0][chId].append( self.trainedData[iter][chId] ) 
                                                          
        
        if ( 0 ) :
            print ( "Bass1 Data Phrase : 1" ) 
            for chId in self.Chords[0] : 
                print ( "\tChord Id: ", chId ) 
                for item in self.Chords[0][chId] : 
                    print ( "\t\tItem Num: 0 Data: ", item ) 
            print() 
                

        return self.Chords
        


    def printTrainedData ( self ) : 

        print ( "Bass1" ) 
        print ( "\tPhrase : 1" ) 
        for chId in self.Chords[0] : 
            print ( "\t\tChord Id: ", chId, "Data: ", self.Chords[0][chId] ) 
        print() 
