from __future__ import print_function

import sys
import copy
import random
import MusicTheory
import TypesOfBassRhythms

numBeats = 16
beatAdderList = [3, 6]
stack = [ 1 ] 

resetBeat = 9
forbiddenBeat = 10 
finalList = []


def CreateBassRhythms ( type, tse ) : 
    
    global numBeats 
    numBeats  = TypesOfBassRhythms.TSERhythmInfo[tse][type]['numBeats'] 

    type = 'popRhythms' 
    global beatAdderList
    beatAdderList = TypesOfBassRhythms.TSERhythmInfo[tse][type]['beatAdderList'] 

        
    for adder in beatAdderList : 
        recursiveFunction ( 1, adder ) 
   


    for item in finalList : 
        if ( random.randint ( 0, 100 ) > 50 ) : 
            rhyIndex = random.randint (0, len(item)-1 ) 
            item[rhyIndex] = str(item[rhyIndex]) + "Rest"


    if ( 0 ) : 
        print()
        for item in finalList : 
            print ( item ) 

    return finalList

def recursiveFunction ( beat, adder ) : 
            
    if ( 0 ) : 
        print ( "I am here 2: beat: ", beat, "adder: ", adder, "stack: ", stack ) 

    if ( beat  >= numBeats ) : 
        #print ( "Done: ", stack ) 
        finalList.append ( copy.deepcopy(stack) ) 

        return -1
    elif ( beat + adder > numBeats ) : 
        #print ( "Done: ", stack ) 
        finalList.append ( copy.deepcopy(stack) ) 

        return -1
    else :
        beat += adder 

        if ( beat == forbiddenBeat ) : 
            beat = resetBeat

        stack.append ( beat ) 
        if ( 0 ) : 
            print ( "I am here 1: beat: ", beat, "adder: ", adder, "stack: ", stack ) 

    #sys.exit(0) 

    for adder1 in beatAdderList : 
        if ( 0 ) : 
            print ( "Beat: ", beat, "Adder1: ", adder1 ) 

        ret = recursiveFunction ( beat, adder1 ) 
        if ( ret == -1 ) : 
            break 
    

    del ( stack[-1] ) 
