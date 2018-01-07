from __future__ import print_function
import sys
import copy
import random
import collections
import DrumConstants
from Skeleton import Constants

def run ( BeatInfo, Patterns, tse, rhythmSpeed, pl ) : 
    if ( 0 ) : 
        print ( "Hihat Drums" ) 

    numBeats = Constants.TSEs[tse]['num16thBeats'] 
    numPatterns = len(Patterns)  # number of patterns to choose from for a normal measure that is not an eop measure or eos measure


    HihatDrum = collections.OrderedDict()   

    HihatDrum['regMeasure'] = collections.OrderedDict()    # this is the normal hihat drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        HihatDrum['regMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            prob     = BeatInfo[beatNum]['hihat']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['hihat']['velocityMin'], BeatInfo[beatNum]['hihat']['velocityMax'] )  
            instrument = random.choice ( DrumConstants.hihatPieces )                                                                                                                                                                                                                                                                                                   


        
            if ( rhythmSpeed == 'slow' and (beatNum % 4) != 1 ) :  # only look at quarter notes
                prob = -1
                
            if ( 0 ) : 
                print ( "Beat: ", beatNum, "Prob: ", prob, "randVal: ", randval , "Velocity: ", velocity , beatNum%4 ) 
                
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            HihatDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['high'][instrument], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )
            HihatDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['high'][instrument], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )

    HihatDrum['eopMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eopStartBeat = Patterns[patternNum]['eopStartBeat'] 
        HihatDrum['eopMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eopStartBeat ) :    # this beat will be filled in by eopFill

                HihatDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['high'][instrument], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )
                HihatDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['high'][instrument], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )

            else : 
                
                data = copy.deepcopy(HihatDrum['regMeasure'][patternNum][cnt]) 
                HihatDrum['eopMeasure'][patternNum].append (data) 
                data = copy.deepcopy(HihatDrum['regMeasure'][patternNum][cnt+1]) 
                HihatDrum['eopMeasure'][patternNum].append (data) 
            cnt += 2

    HihatDrum['eosMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of Section measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eosStartBeat = Patterns[patternNum]['eosStartBeat'] 
        HihatDrum['eosMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eosStartBeat ) :    # this beat will be filled in by eosFill

                HihatDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['high'][instrument], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )
                HihatDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['high'][instrument], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )

            else : 
                
                data = copy.deepcopy(HihatDrum['regMeasure'][patternNum][cnt]) 
                HihatDrum['eosMeasure'][patternNum].append (data) 
                data = copy.deepcopy(HihatDrum['regMeasure'][patternNum][cnt+1]) 
                HihatDrum['eosMeasure'][patternNum].append (data) 
            cnt += 2

    if ( 0 ) : 
        print ( "Hihat Drum" ) 
        for patternNum in range(numPatterns) : 
            print ( "\tPattern Num: ", patternNum ) 
            for measureType in HihatDrum : 
                print ( "\t\tMeasure Type: ", measureType ) 
                for item in range( 0, numBeats*2, 2 ) : 
                    print ( "Item: ", item, HihatDrum[measureType][patternNum][item] ) 
                print() 

    #HihatDrum => HihatDrum[measureType][numPatterns][item] ) 

    return HihatDrum


