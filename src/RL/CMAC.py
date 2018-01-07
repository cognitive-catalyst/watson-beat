from __future__ import print_function

import random
import Tiles

class CMAC: 
    def __init__ ( self ) : 

        self.alpha = 0.0 

        self.floatInputs = [] 
        self.numFloatInputs = 0 
 
        self.intInputs = [] 
        self.numIntInputs = 0 
        
        self.tiles = []
        self.numTilings = 0 

        self.u = []  # CMAC arrays        
        self.memorySize = 0  # num entries in CMAC arrays

        self.tableDimensionality = 0 
        return


    def __init__ ( self, alpha,  numFloatInputs, numIntInputs, memorySize, gamma, numTilings, tableDimensionality ) : 
        
        self.alpha = alpha 

        self.numFloatInputs = numFloatInputs 
        self.floatInputs = [] 
        for i in range( numFloatInputs ) : 
            self.floatInputs.append ( 0.0 ) ; 

        self.numIntInputs = numIntInputs 
        self.intInputs = [] 
        for i in range( numIntInputs ) : 
            self.intInputs.append ( 0 ) ; 
 
        self.numTilings = numTilings
        self.tiles = []        
        for i in range ( numTilings ) :
            self.tiles.append ( 0 ) 

    
        self.memorySize = memorySize 
        self.u = []  # CMAC arrays        
        for i in range ( memorySize ) :
            #self.u.append ( 1.0 / ( 1.0 - gamma ) )                
            #self.u.append ( 1.0 / ( 1.0 - gamma - 0.01 ) ) # this is to account for the fact that gamma = 1 for episodic tasks, and gamma < 1 for continuing tasks.
            #self.u.append ( random.randint ( 1, 20 ) ) #1.0 / ( 1.0 - gamma - 0.01 ) ) # this is to account for the fact that gamma = 1 for episodic tasks, and gamma < 1 for continuing tasks.
            self.u.append ( 2 ) #1.0 / ( 1.0 - gamma - 0.01 ) ) # this is to account for the fact that gamma = 1 for episodic tasks, and gamma < 1 for continuing tasks.
            #print ( "Memory Size: ", memorySize, "self.u[", i, "]", self.u[i], "Gamma:" , gamma, "1.0-gamma", 1.0 - gamma ) 

        
        self.tableDimensionality = tableDimensionality 

        #self.printCMACParams ( ) 

        self.Tile = Tiles.Tiles()
        return

    
    def setFloatInputs ( self, index, val ) : 
        self.floatInputs[index] = val
        return


    def setIntInputs ( self, index, val ) :
        self.intInputs[index] = val 
        return 


    def predict ( self ) :
        for i in range ( self.numTilings ) :
            self.tiles[i] = 0  

        #print ( "CMAC Tiles Before: ", self.tiles, "Float Inputs: ", self.floatInputs, "Int Inputs: ", self.intInputs  ) 
        self.tiles = self.Tile.GetTiles ( self.tiles,  self.numTilings, self.memorySize, self.floatInputs, self.numFloatInputs, self.intInputs, self.numIntInputs ) 
        #print ( "CMAC Tiles After: ", self.tiles ) 
        # calculate the sum of all the indexed CMAC tiles
        sum = 0.0 
        for i in range ( self.numTilings ) : 
            sum += self.u[self.tiles[i]] 
            #print ( "Predict: i: ", i, "sum: ", sum, "tiles[i]: ", self.tiles[i] , "self.u[self.tiles[i]] : ", self.u[self.tiles[i]] ) 
        #print ( "Predict Q Value: ", sum ) 
        return sum 
        
    def update ( self, target ) : 
        #print ( "Update CMAC Tiles Before: ", self.tiles ) 
        self.tiles = self.Tile.GetTiles (  self.tiles,  self.numTilings, self.memorySize, self.floatInputs, self.numFloatInputs, self.intInputs, self.numIntInputs )  
        #print ( "Update CMAC Tiles After: ", self.tiles ) 
        # calculate the sum of all the indexed CMAC tiles
        pred = 0.0 
        for i in range ( self.numTilings ) : 
            pred += self.u[self.tiles[i]] 
        
        #print ( "r + gamma * NewQ: ", target, "Old Q: ", pred, "Diff: ", (self.alpha/self.numTilings) * ( target - pred ) )        
        # train the cmac arrays
        for i in range ( self.numTilings ) : 
            #print ( "Tile Num: ", self.tiles[i], "Tile Value before: ", self.u[self.tiles[i]] ) 
            self.u[self.tiles[i]] += ( (self.alpha/self.numTilings) * ( target - pred ) )         
            #print ( "Tile Num: ", self.tiles[i], "Tile Value after: ", self.u[self.tiles[i]] ) 
        return 
        
    def printCMACParams ( self ) : 
        print ( "Initializing CMAC Arrays" ) 
        print ( "Float Inputs; " , self.floatInputs , self.numFloatInputs,  "Int Inputs; " , self.intInputs , self.numIntInputs, "Size of CMAC Arrays (memory size) : " , self.memorySize,  "Tiles: ", self.tiles, self.numTilings ) 
        print() 
        return 


        print ( "Float Inputs; " , self.floatInputs , self.numFloatInputs ) 
        print ( "Int Inputs; " , self.intInputs , self.numIntInputs ) 
        print ( "Size of CMAC Arrays (memory size) : " , self.memorySize ) 
        print ( "Tiles: ", self.tiles, self.numTilings ) 
