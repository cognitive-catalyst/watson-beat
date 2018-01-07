from __future__ import print_function
from copy import deepcopy

import sys
import random

import CMAC
import State


import Skeleton.Constants



class QLearning:
    
    def __init__ ( self, numFeatures, features, numActions, memorySize, epsilon, numTilings, tableDimensionality, delta, alpha, gamma, layerObj ) :

        self.layerObj = layerObj

        self.bellmanError = 0.0 
        self.numFeatures = numFeatures
        self.numActions  = numActions
        self.delta    = delta
        self.gamma    = gamma
        self.alpha    = alpha
        self.epsilon  = epsilon

        self.features = [] 
        for i in range(numFeatures) : 
            self.features.append ( features[i] ) 

        # initialize current and next state 
        self.initializeState () 

        # sanity check print function
        #self.printQLearningParams () 
        
        # initialize CMAC arrays
        self.cmac = CMAC.CMAC ( alpha, numFeatures, 1, memorySize, gamma, numTilings, tableDimensionality ) 

    def initializeState ( self ) :

        self.currentState = State.State( self.numFeatures ) 
        self.nextState = State.State( self.numFeatures ) 
        self.currentReward = 1.0
        self.nextReward = 0.0

        self.currentAction = self.layerObj.defaultAction 
        self.nextAction    = self.layerObj.defaultAction 

        self.T = State.Tuple (  self.currentState, self.currentAction, self.currentReward, self.nextState, self.nextAction )         


    # initialize CMAC inputs based on the current state-action pair
    def populateCMACs ( self, s, a ) :
        for i in range ( self.numFeatures ) : 
            val = s.getStat ( self.features[i] ) 
            self.cmac.setFloatInputs ( i, 1.0 * val ) 
            
        self.cmac.setIntInputs ( 0, a ) 
        if ( 0 ) : 
            print ( "PopulateCMACs: FloatInputs: ", self.cmac.floatInputs, "InttInputs: ", self.cmac.intInputs ) 
        return 


    def predictQFactor ( self, s, a ) :
        #print ( "\nPredict Q Factor: ", s.stats, a ) 
        # populate CMACs
        self.populateCMACs ( s, a ) 
        
        # get q value prediction for state s and action a
        q = self.cmac.predict ()         
        return q


    def updateRL ( self, nextReward, nextAction, data ) : # for bass1 data will be : chord, scale

        self.nextState = self.layerObj.getNextState ( nextAction, data )   # for bass1 data will be :  chord, scale

        self.nextAction = self.layerObj.ReverseActions[nextAction]
        self.nextReward = nextReward
        

        self.T.setCurrentState  ( self.currentState ) 
        self.T.setCurrentAction ( self.currentAction ) 
        self.T.setReward ( self.currentReward ) 
        self.T.setNextState (self.nextState ) 
        self.T.setNextAction (self.nextAction ) 
        
        if ( 0 ) : 
            print ( "Update RL", "next reward: ", self.nextReward, "current Reward: ", self.currentReward ) 
        self.updateSarsa ( self.T ) 
        
        self.currentState  = deepcopy(self.nextState)
        self.currentAction = deepcopy(self.nextAction)
        self.currentReward = deepcopy(self.nextReward)


    def updateSarsa ( self, T ) :
        currentState = T.getCurrentState() 
        currentAction = T.getCurrentAction() 
        reward = T.getReward()
        
        nextState = T.getNextState() 
        nextAction = T.getNextAction() 
        
        #Get Q( s', a' )
        if ( 0 ) : 
            print ( "Populate CMACs for nextState: " ) 
        self.populateCMACs ( nextState, nextAction ) 
        nextQ = self.cmac.predict() 

        #Get Q( s, a )
        if ( 0 ) : 
            print ( "Populate CMACs for currentState: " ) 
        self.populateCMACs ( currentState, currentAction ) 
        oldQ = self.cmac.predict() 
        
        self.cmac.update ( reward + self.gamma * nextQ )
        if ( 0 ) : 
            print ( "OldQ: ", oldQ, "nextQ: ", nextQ, "reward + self.gamma * nextQ: ", reward + self.gamma * nextQ ) 

        return 
    
    
    def printQLearningParams ( self ) :
        #print ( "\nInitializing QLearning Object for layer: ", self.layerObj.desc ) 
        #print ( "Bellman Error: ", self.bellmanError, "Num Features: ", self.numFeatures, "Num Actions: ", self.numActions, "Delta: ", self.delta, "Gamma: ", self.gamma,  "Alpha: ", self.alpha ) 
        
        return 


        print ( "Bellman Error: ", self.bellmanError ) 
        print ( "Num Features: ", self.numFeatures  ) 
        print ( "Num Actions: ", self.numActions ) 
        print ( "Delta: ", self.delta ) 
        print ( "Gamma: ", self.gamma ) 
        print ( "Alpha: ", self.alpha ) 



    def printCurrentState ( self ) : 
        print ( "Printing CurrentState Stats: ", self.currentState.stats ) 

    def printNextState ( self ) : 
        print ( "Printing NextState Stats   : ", self.nextState.stats ) 
