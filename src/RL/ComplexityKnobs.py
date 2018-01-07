from __future__ import print_function


Actions = { 

    'bass1': {
        0:'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP',             
        1:'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP',             
        2:'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP',             
        3:'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY', 
        },

    'bass2': {
        'simple' : {
            0:'PLAY_HOME_NOTE',
            1:'PLAY_FIFTH_NOTE',
            2:'PLAY_OCTAVE_UP',           
            }, 

        'complex' : {
            0:'PLAY_HOME_NOTE',
            1:'PLAY_FIFTH_NOTE',
            2:'PLAY_OCTAVE_UP',           
            #3:'CHROMATICS',
            }, 
        },


    'bass3': {
        'simple' : {
            0:'PLAY_HOME_NOTE',
            1:'PLAY_FIFTH_NOTE',
            2:'PLAY_OCTAVE_UP',           
            }, 
        'complex' : {
            0:'PLAY_HOME_NOTE',
            1:'PLAY_FIFTH_NOTE',
            2:'PLAY_OCTAVE_UP',           
            #3:'CHROMATICS',
            }, 
        },


    'melody5': { 
        0: 'PLAY_HOME_NOTE', 
        1: 'PLAY_CHORD_TONE', 
        2: 'PLAY_PASSING_TONE_UP', 
        3: 'PLAY_PASSING_TONE_DOWN', 
        4: 'PLAY_NEIGHBOR_TONE_UP', 
        5: 'PLAY_NEIGHBOR_TONE_DOWN', 
        6: 'PLAY_CHORD_TO_CHORD_UP',
        7: 'PLAY_CHORD_TO_CHORD_DOWN', 
        },
    } # End Actions

ReverseActions = { 
    
    'bass1': {

        'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': 0,             
        'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': 1,             
        'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': 2,             
        'PLAY_CHORD_PROGRESSION_TONE_FOR_PRIMARY_KEY': 3,
        },

    'bass2': { 
        'simple' : {
            'PLAY_HOME_NOTE':0,
            'PLAY_FIFTH_NOTE':1,            
            'PLAY_OCTAVE_UP':2,           
            }, 
        'complex' : {
            'PLAY_HOME_NOTE':0,
            'PLAY_FIFTH_NOTE':1,            
            'PLAY_OCTAVE_UP':2,           
            #'CHROMATICS': 3,
            }, 
        },

    'bass3': { 
        'simple' : {
            'PLAY_HOME_NOTE':0,
            'PLAY_FIFTH_NOTE':1,            
            'PLAY_OCTAVE_UP':2,           
            }, 
        'complex' : {
            'PLAY_HOME_NOTE':0,
            'PLAY_FIFTH_NOTE':1,            
            'PLAY_OCTAVE_UP':2,           
            #'CHROMATICS': 3,
            }, 
        },


    'melody5': { 
        'PLAY_HOME_NOTE'           : 0,
        'PLAY_CHORD_TONE'          : 1,
        'PLAY_PASSING_TONE_UP'     : 2,
        'PLAY_PASSING_TONE_DOWN'   : 3, 
        'PLAY_NEIGHBOR_TONE_UP'    : 4,
        'PLAY_NEIGHBOR_TONE_DOWN'  : 5, 
        'PLAY_CHORD_TO_CHORD_UP'   : 6, 
        'PLAY_CHORD_TO_CHORD_DOWN' : 7, 

        },


    } # End ReverseActions




def setKnobs ( layer, complexity, layerParams ) : 

    knobs = None
    if ( layer == 'bass1' ) : 
        actions = Actions[layer]
        reverseActions = ReverseActions[layer]

        minPenalty = layerParams['minPenalty']
        maxPenalty = layerParams['maxPenalty']
        #self.trueMaxPenalty = -30   # ( -8 + ( -10 ) + ( -6 * 2 ) ) = ( -30 )
        #self.penaltyBase = ( self.trueMaxPenalty * -1 ) + 1  # why 31, beacuse the adder for making all penalties positive is 31. why 31, because the maximum penalty is -30 and the min penalty = 3 
        #self.penaltyMin  = self.penaltyBase + self.trueMinPenalty # so min penalty after adder = 3+31 = 34
        #self.penaltyMax  = self.penaltyBase + self.trueMaxPenalty # so max penalty after adder = -30 + 31 = 1

        # min penalty = 3, max penalty = -30. adder = 31. so min penalty after adder = 34, max penalty = 1. so higher the number less is the penalty, smaller is the cp jump 

        #self.trueMaxPenalty = -24   # ( 0 + (-5) + (-19) ) 
        #self.trueMinPenalty =  4    # ( 4 + (0) + (0) ) 
        #self.penaltyBase = ( self.trueMaxPenalty * -1 ) + 1  # why 25, beacuse the adder for making all penalties positive is 25. why 25, because the maximum penalty is -24 and the min penalty = 4 
        #self.penaltyMin  = self.penaltyBase + self.trueMinPenalty # so min penalty after adder = 4+25 = 29
        #self.penaltyMax  = self.penaltyBase + self.trueMaxPenalty # so max penalty after adder = -24 + 25 = 1

        # min penalty = 29, max penalty = 1.  higher the number, less is the penalty, smaller is the cp jump 

        if ( complexity == 'super_simple' ) : 
            knobs = {
                'syncopation'      : 'none',  #high, low, medium
                'cprogJumpLow'     : minPenalty-5,
                'cprogJumpHigh'    : minPenalty,   
                'CProgComplexity'  : [ 'obvious' ]
                }                
        elif ( complexity == 'simple' ) : 
            knobs = {
                'syncopation'      : 'none',  #high, low, medium
                'cprogJumpLow'     : minPenalty-10,
                'cprogJumpHigh'    : minPenalty,   
                'CProgComplexity'  : [ 'obvious' ]
                }                

        elif ( complexity == 'semi_complex'  ) : 
            knobs = {
                'syncopation'      : 'none',  #high, low, medium
                'cprogJumpLow'     : minPenalty-12,
                'cprogJumpHigh'    : minPenalty-6,   
                'CProgComplexity'  : [ 'obvious', 'unusual' ]
                }                            
        elif ( complexity == 'complex' ) : 

            knobs = {
                'syncopation'     : 'none',  #high, low, medium
                'cprogJumpLow'     : minPenalty-24,
                'cprogJumpHigh'    : minPenalty-12,   
                'CProgComplexity' : [ 'unusual', 'obscure' ]
                }                
            
    # end if layer == bass1
    elif ( layer == 'bass2' ) : 

        if ( complexity == 'super_simple' ) : 
            actions = Actions[layer]['simple']
            reverseActions = ReverseActions[layer]['simple']
            
            knobs = {
                'chordToneThresholdHigh'   : 0.1,
                'nonChordToneThresholdHigh': 0.05,

                'chordToneThresholdLow'    : 0.95,
                'nonChordToneThresholdLow' : 0.00,
                }

        elif ( complexity == 'simple' ) : 
            actions = Actions[layer]['simple']
            reverseActions = ReverseActions[layer]['simple']
            
            knobs = {
                'chordToneThresholdHigh'   : 0.1,
                'nonChordToneThresholdHigh': 0.10,

                'chordToneThresholdLow'    : 0.90,
                'nonChordToneThresholdLow' : 0.00,
                }

        elif ( complexity == 'semi_complex' ) : 
            actions = Actions[layer]['complex']
            reverseActions = ReverseActions[layer]['complex']
            reverseActions = ReverseActions[layer]['simple']
            
            knobs = {
                'chordToneThresholdHigh'   : 0.90,
                'nonChordToneThresholdHigh': 0.20,

                'chordToneThresholdLow'    : 0.80,
                'nonChordToneThresholdLow' : 0.10,
                }

        elif ( complexity == 'complex' ) : 
            actions = Actions[layer]['complex']
            reverseActions = ReverseActions[layer]['complex']
            
            knobs = {
                'chordToneThresholdHigh'   : 0.80,
                'nonChordToneThresholdHigh': 0.40,

                'chordToneThresholdLow'    : 0.60,
                'nonChordToneThresholdLow' : 0.10,
                }

    # end if layer == bass2

    elif ( layer == 'bass3' ) : 

        if ( complexity.endswith('simple') ) : 
            actions = Actions[layer]['simple']
            reverseActions = ReverseActions[layer]['simple']
            
            knobs = {}

        else : 
            actions = Actions[layer]['complex'] 
            reverseActions = ReverseActions[layer]['complex']
            
            knobs = {}

    # end if layer == bass3


    elif ( layer == 'melody5' ) : 
        actions = Actions[layer]
        reverseActions = ReverseActions[layer]

        
        if ( complexity == 'super_simple' ) : 
            knobs = {
                'chordToneThresholdHigh'   : 0.1,
                'nonChordToneThresholdHigh': 0.10,

                'chordToneThresholdLow'    : 0.90,
                'nonChordToneThresholdLow' : 0.00,

                'gestureMvmt' : 8 #'verySmall', stay within 8 halfsteps of base home note
                }                
        elif ( complexity == 'simple' ) : 
            knobs = {

                'chordToneThresholdHigh'   : 0.1,
                'nonChordToneThresholdHigh': 0.10,

                'chordToneThresholdLow'    : 0.90,
                'nonChordToneThresholdLow' : 0.00,

                'gestureMvmt' : 12 #'small', stay within 12 halfsteps of base home note

                }                
        elif ( complexity == 'semi_complex'  ) : 
            knobs = {
                'chordToneThresholdHigh'   : 0.60,
                'nonChordToneThresholdHigh': 0.60,

                'chordToneThresholdLow'    : 0.45,
                'nonChordToneThresholdLow' : 0.45,

                'gestureMvmt' : 18 #'medium', stay within 18 halfsteps of base home note

                }                
        elif ( complexity == 'complex' ) : 
            knobs = {

                'chordToneThresholdHigh'   : 0.1,
                'nonChordToneThresholdHigh': 0.10,

                'chordToneThresholdLow'    : 0.90,
                'nonChordToneThresholdLow' : 0.00,

                'gestureMvmt' : 24 #'medium', stay within 24 halfsteps of base home note

                }                
    # end if layer == melody5


    return knobs, actions, reverseActions
