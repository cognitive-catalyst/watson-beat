from __future__ import print_function
import sys
import copy
import random
import collections
import DrumConstants
from Skeleton import Constants

def run ( BeatInfo, Patterns, tse, rhythmSpeed, pl, rhythms ) : 

    if ( 0 ) : 
        print ( "Latin Pop Drums" ) 

    numBeats = Constants.TSEs[tse]['num16thBeats'] 
    numPatterns = len(Patterns)  # number of patterns to choose from for a normal measure that is not an eop measure or eos measure

    LatinPopDrum = collections.OrderedDict()    

    LatinPopDrum['regMeasure'] = collections.OrderedDict()    # this is the normal kick drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        LatinPopDrum['regMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum in rhythms[0] ) : 
                velocity = random.randint ( BeatInfo[beatNum]['kick']['velocityMin'], BeatInfo[beatNum]['kick']['velocityMax'] )  
            else : 
                velocity = 0 
                
            if ( 0 ) : 
                print ( "Beat: ", beatNum, "Velocity: ", velocity ) 
                
                                
            LatinPopDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
            LatinPopDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )


    LatinPopDrum['eopMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eopStartBeat = Patterns[patternNum]['eopStartBeat'] 
        LatinPopDrum['eopMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum in rhythms[1] ) : 
                velocity = random.randint ( BeatInfo[beatNum]['kick']['velocityMin'], BeatInfo[beatNum]['kick']['velocityMax'] )  
            else : 
                velocity = 0 
                
            if ( beatNum >= eopStartBeat ) :    # this beat will be filled in by eopFill

                LatinPopDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                LatinPopDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            else : 

                LatinPopDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                LatinPopDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                
            cnt += 2

            if ( 0 ) : 
                print ( "Beat: ", beatNum, "Velocity: ", velocity, "eopStartBeat:", eopStartBeat ) 
                

    LatinPopDrum['eosMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eosStartBeat = Patterns[patternNum]['eosStartBeat'] 
        LatinPopDrum['eosMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum in rhythms[1] ) : 
                velocity = random.randint ( BeatInfo[beatNum]['kick']['velocityMin'], BeatInfo[beatNum]['kick']['velocityMax'] )  
            else : 
                velocity = 0 
                
            if ( beatNum >= eosStartBeat ) :    # this beat will be filled in by eosFill

                LatinPopDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                LatinPopDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            else : 

                LatinPopDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                LatinPopDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                
            cnt += 2

            if ( 0 ) : 
                print ( "Beat: ", beatNum, "Velocity: ", velocity, "eosStartBeat:", eosStartBeat ) 
                                

    if ( 0 ) : 
        print()
        print ( "LatinPop Drum" ) 
        for patternNum in range(numPatterns) : 
            print ( "\tPattern Num: ", patternNum ) 
            for measureType in LatinPopDrum : 
                print ( "\t\tMeasure Type: ", measureType ) 
                for item in range( 0, numBeats*2, 2 ) : 
                    print ( "\t\t\tItem: ", item, LatinPopDrum[measureType][patternNum][item] ) 
                print() 



    return LatinPopDrum

