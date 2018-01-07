from __future__ import print_function
import sys 
import math
import random


MAX_NUM_VARS = 128
MAX_NUM_COORDS = 100
MaxLongInt = 2147483647
RNDLIMIT = 2048 #16  #2048
prn = False


class Tiles: 
    def __init__ ( self ) : 
        
        self.firstCall = True        
        self.rndseq = []
        for i in range ( RNDLIMIT ) :
            self.rndseq.append( 0  )
        return 

    def mod ( self, n, k ) :
        if ( n >= 0 ) : 
            return n%k 
        else :
            return ( k-1-((-n-1)%k) )

    def GetTiles ( self, tiles, numTilings, memorySize, floats, numFloats, ints, numInts ) :

        coordinates = []
        qstate = [] 
        base = [] 
        numCoordinates = numFloats + numInts + 1

        for i in range(numFloats) : 
            coordinates.append ( 0 ) 
            qstate.append ( int ( math.floor( floats[i] * numTilings )) )
            base.append ( 0 ) 

        coordinates.append ( 0 ) 
        for i in range(numInts) : 
            coordinates.append ( ints[i] ) 

        for j in range ( numTilings ) : 
            for i in range ( numFloats ) : 
                if ( prn ) : 
                    print ( "Tile Num: ", j, "Float Num: ", i, "QState: ", qstate[i], "base[i]: ", base[i], "qstate[i]-base[i]: ", qstate[i]-base[i], "mod numtilings: ", self.mod ( qstate[i]-base[i], numTilings ) ) 
                coordinates[i] = qstate[i] - self.mod ( qstate[i]-base[i], numTilings ) 
                base[i] += 1 + ( 2 * i ) 
            coordinates[i+1] = j
            
            if ( prn ) : 
                print ( "Tile Num: j: ", j,  "Get Tiles: Before: coordinates: ", coordinates, " QState: ", qstate ) 
            tiles[j] = self.hash_UNH ( coordinates, numCoordinates, memorySize, 449 ) 
            if ( prn ) : 
                print() 
        if ( prn ) : 
            print ( "Get Tiles: After: coordinates: ", coordinates,  " QState: ", qstate  ) 

        #sys.exit(0) 
        return tiles



    def hash_UNH ( self, ints, numInts, memSize, increment ) : 
        sum = 0 
        #print ( "Ints: ", ints ) 
        if ( self.firstCall ) :
            for k in range ( RNDLIMIT ) : 
                self.rndseq[k] = 0 
                for i in range ( 2 ) : 
                    #self.rndseq[k] = ( self.rndseq[k] << 8 ) | ( random.randint ( 0, 32767 ) | 0xff )  
                    #self.rndseq[k] = ( self.rndseq[k] << 2 ) | ( random.randint ( 0, 2047 ) | 0xff )  
                    self.rndseq[k] =  random.randint ( 0, 32767 ) 
            #print ( self.rndseq ) 
            #sys.exit(0)
            self.firstCall = False

        for i in range( numInts ) : 
            index = ints[i]
            #print ( "1: ", index ) 
            index += ( increment * i ) 
            #print ( "2: ", index ) 
            index %= RNDLIMIT 
            #print ( "3: ", index ) 
            while ( index < 0 ) : 
                index += RNDLIMIT 
            #print ( "4: ", index ) 
            sum += self.rndseq[int(index)]
            #print ( "5: ", sum ) 

        index = int(sum) % memSize 
        #print ( sum, memSize, index ) 
        while ( index < 0 ) : 
            index += memSize



        return ( index ) 


