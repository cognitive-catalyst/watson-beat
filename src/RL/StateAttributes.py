from __future__ import print_function

#State attributes for the different layers




StateAttributes = { 

    'bass1': {
        
        'HOME_CHORD_MOVEMENT_DISTANCE': 0, 

        }, 

    'bass2': {
               
        'DURATION_CHORD_TONES_FOR_CHORD_LENGTH': 0, 
        
        'DURATION_NON_CHORD_TONES_FOR_CHORD_LENGTH': 1, 

        }, 

    'melody5': {
               
        'DURATION_CHORD_TONES_FOR_CHORD_LENGTH': 0, 
        
        'DURATION_NON_CHORD_TONES_FOR_CHORD_LENGTH': 1,         

        'HOME_GESTURE_MOVEMENT_DISTANCE': 2, 

        }, 


    }


def printStateAttributes ( layer ) : 
    
    print ( "Printing State Attributes for layer: " , layer ) 
    for key in StateAttributes[layer] : 
        print ( key ) 

    print() 


