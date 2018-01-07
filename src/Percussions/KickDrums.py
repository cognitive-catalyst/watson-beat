from __future__ import print_function
import sys
import copy
import random
import collections
import DrumConstants
from Skeleton import Constants

def run ( BeatInfo, Patterns, tse, rhythmSpeed, pl ) : 
    if ( 0 ) : 
        print ( "Kick Drums" ) 

    numBeats = Constants.TSEs[tse]['num16thBeats'] 
    numPatterns = len(Patterns)  # number of patterns to choose from for a normal measure that is not an eop measure or eos measure

    KickDrum = collections.OrderedDict()    

    KickDrum['regMeasure'] = collections.OrderedDict()    # this is the normal kick drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        KickDrum['regMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            prob     = BeatInfo[beatNum]['kick']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['kick']['velocityMin'], BeatInfo[beatNum]['kick']['velocityMax'] )  
        
            if ( rhythmSpeed == 'slow' and (beatNum % 4) != 1 ) :  # only look at quarter notes
                prob = -1
                
            if ( 0 ) : 
                print ( "Beat: ", beatNum, "Prob: ", prob, "randVal: ", randval , "Velocity: ", velocity , beatNum%4 ) 
                
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            KickDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
            KickDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

    KickDrum['eopMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eopStartBeat = Patterns[patternNum]['eopStartBeat'] 
        KickDrum['eopMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eopStartBeat ) :    # this beat will be filled in by eopFill

                KickDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                KickDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            else : 
                
                data = copy.deepcopy(KickDrum['regMeasure'][patternNum][cnt]) 
                KickDrum['eopMeasure'][patternNum].append (data) 
                data = copy.deepcopy(KickDrum['regMeasure'][patternNum][cnt+1]) 
                KickDrum['eopMeasure'][patternNum].append (data) 
            cnt += 2

    KickDrum['eosMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of Section measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eosStartBeat = Patterns[patternNum]['eosStartBeat'] 
        KickDrum['eosMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eosStartBeat ) :    # this beat will be filled in by eosFill

                KickDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                KickDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            else : 
                
                data = copy.deepcopy(KickDrum['regMeasure'][patternNum][cnt]) 
                KickDrum['eosMeasure'][patternNum].append (data) 
                data = copy.deepcopy(KickDrum['regMeasure'][patternNum][cnt+1]) 
                KickDrum['eosMeasure'][patternNum].append (data) 
            cnt += 2

    if ( 0 ) : 
        print ( "Kick Drum" ) 
        for patternNum in range(numPatterns) : 
            print ( "\tPattern Num: ", patternNum ) 
            for measureType in KickDrum : 
                print ( "\t\tMeasure Type: ", measureType ) 
                for item in range( 0, numBeats*2, 2 ) : 
                    print ( "Item: ", item, KickDrum[measureType][patternNum][item] ) 
                print() 

    #KickDrum => KickDrum[measureType][numPatterns][item] ) 

    return KickDrum


