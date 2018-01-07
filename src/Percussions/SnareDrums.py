from __future__ import print_function
import sys
import copy
import random
import collections
import DrumConstants
from Skeleton import Constants

def run ( BeatInfo, Patterns, tse, rhythmSpeed, pl ) : 
    if ( 0 ) : 
        print ( "Snare Drums" ) 

    numBeats = Constants.TSEs[tse]['num16thBeats'] 
    numPatterns = len(Patterns)  # number of patterns to choose from for a normal measure that is not an eop measure or eos measure

    SnareDrum = collections.OrderedDict() 

    SnareDrum['regMeasure'] = collections.OrderedDict()    # this is the normal snare drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        SnareDrum['regMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            prob     = BeatInfo[beatNum]['snare']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['snare']['velocityMin'], BeatInfo[beatNum]['snare']['velocityMax'] )  
        
            if ( rhythmSpeed == 'slow' and (beatNum % 4) != 1 ) :  # only look at quarter notes
                prob = -1
                
            if ( 0 ) : 
                print ( "Beat: ", beatNum, "Prob: ", prob, "randVal: ", randval , "Velocity: ", velocity , beatNum%4 ) 
                
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            SnareDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )
            SnareDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )

    SnareDrum['eopMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eopStartBeat = Patterns[patternNum]['eopStartBeat'] 
        SnareDrum['eopMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eopStartBeat ) :    # this beat will be filled in by eopFill

                SnareDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )
                SnareDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )

            else : 
                
                data = copy.deepcopy(SnareDrum['regMeasure'][patternNum][cnt]) 
                SnareDrum['eopMeasure'][patternNum].append (data) 
                data = copy.deepcopy(SnareDrum['regMeasure'][patternNum][cnt+1]) 
                SnareDrum['eopMeasure'][patternNum].append (data) 
            cnt += 2

    SnareDrum['eosMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of Section measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eosStartBeat = Patterns[patternNum]['eosStartBeat'] 
        SnareDrum['eosMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eosStartBeat ) :    # this beat will be filled in by eosFill

                SnareDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )
                SnareDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )

            else : 
                
                data = copy.deepcopy(SnareDrum['regMeasure'][patternNum][cnt]) 
                SnareDrum['eosMeasure'][patternNum].append (data) 
                data = copy.deepcopy(SnareDrum['regMeasure'][patternNum][cnt+1]) 
                SnareDrum['eosMeasure'][patternNum].append (data) 
            cnt += 2

    if ( 0 ) : 
        print ( "Snare Drum" ) 
        for patternNum in range(numPatterns) : 
            print ( "\tPattern Num: ", patternNum ) 
            for measureType in SnareDrum : 
                print ( "\t\tMeasure Type: ", measureType ) 
                for item in range( 0, numBeats*2, 2 ) : 
                    print ( "Item: ", item, SnareDrum[measureType][patternNum][item] ) 
                print() 

    #SnareDrum => SnareDrum[measureType][numPatterns][item] ) 

    return SnareDrum


