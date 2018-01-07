from __future__ import print_function

import sys
import StateAttributes


class State :
    
    def __init__ ( self, numFeatures ) :
        self.stats = [] 
        # Initialize Stat Array
        for i in range ( numFeatures ) : 
            self.stats.append ( 0.0 ) 
        return 
    
    def setStat ( self, fNum, val ) :
        self.stats[fNum] = val 
        return 

    def getStat ( self, fNum ) : 
        return self.stats[fNum]

    def printStats ( self ) : 
        print ( self.stats ) 
        return 

# defines tuple for temporal difference methods
# <s, a, r, s'>
class Tuple : 
    
    def __init__ ( self ) : 

        # current State 
        self.currentState = State()  

        # current Action
        self.currentAction = 0  # assume current action is a NOP 

        # reward
        self.reward = 0.0 

        # next State 
        self.nextState = State() 
        
        # next action 
        self.nextAction = 0  # assume current action is a NOP 

    def __init__ ( self, currState, currAction, reward, nextState, nextAction ) : 
        self.currentState  = currState 
        self.currentAction = currAction 
        self.reward        = reward 
        self.nextState     = nextState
        self.nextAction    = nextAction
        #self.printTupleParams ()
        return 

    def setCurrentState ( self, state ) : 
        self.currentState = state 
        return

    def getCurrentState ( self ) :
        return self.currentState



    def setCurrentAction ( self, action ) : 
        self.currentAction = action 
        return

    def getCurrentAction ( self ) :
        return self.currentAction
    

    def setReward ( self, reward ) :
        self.reward = reward 
        return

    def getReward ( self ) : 
        return self.reward 



    def setNextState ( self, state ) :
        self.nextState = state
        return

    def getNextState ( self ) :
        return self.nextState



    def setNextAction ( self, action ) : 
        self.nextAction = action
        return

    def getNextAction ( self ) :
        return self.nextAction


    def printTupleParams ( self ) :         
        print ( "\nPrinting RL Tuple Params" ) 
        print ( "Current State: ", self.currentState.stats ) 
        print ( "Next State: ", self.nextState.stats ) 
        print ( "Current Action: ", self.currentAction ) 
        print ( "Next Action: ", self.nextAction ) 
        print ( "Reward: ", self.reward ) 
        
        return 
    


    

