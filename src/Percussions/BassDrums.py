from __future__ import print_function
import sys
import copy
import random
import collections
import DrumConstants
from Skeleton import Constants

def run ( BeatInfo, Patterns, tse, rhythmSpeed, pl ) : 
    if ( 0 ) : 
        print ( "Bass Drums" ) 

    numPatterns = len(Patterns)  # number of patterns to choose from for a normal measure that is not an eop measure or eos measure
    numBeats = Constants.TSEs[tse]['num16thBeats'] 

    BassDrum = collections.OrderedDict() 

    BassDrum['regMeasure'] = collections.OrderedDict()    # this is the normal bass drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        BassDrum['regMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            prob     = BeatInfo[beatNum]['bass']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['bass']['velocityMin'], BeatInfo[beatNum]['bass']['velocityMax'] )  
        
            if ( rhythmSpeed == 'slow' and (beatNum % 4) != 1 ) :  # only look at quarter notes
                prob = -1
                
            if ( 0 ) : 
                print ( "Beat: ", beatNum, "Prob: ", prob, "randVal: ", randval , "Velocity: ", velocity , beatNum%4 ) 
                
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            BassDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['bass'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['bass'], 'pitch': "midi." + DrumConstants.fillNotes['low']['bass'] + "_" + str(DrumConstants.fillNoteOctaves['low']['bass']) } )
            BassDrum['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['bass'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['bass'], 'pitch': "midi." + DrumConstants.fillNotes['low']['bass'] + "_" + str(DrumConstants.fillNoteOctaves['low']['bass']) } )

    BassDrum['eopMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eopStartBeat = Patterns[patternNum]['eopStartBeat'] 
        BassDrum['eopMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eopStartBeat ) :    # this beat will be filled in by eopFill

                BassDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['bass'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['bass'], 'pitch': "midi." + DrumConstants.fillNotes['low']['bass'] + "_" + str(DrumConstants.fillNoteOctaves['low']['bass']) } )
                BassDrum['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['bass'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['bass'], 'pitch': "midi." + DrumConstants.fillNotes['low']['bass'] + "_" + str(DrumConstants.fillNoteOctaves['low']['bass']) } )

            else : 
                
                data = copy.deepcopy(BassDrum['regMeasure'][patternNum][cnt]) 
                BassDrum['eopMeasure'][patternNum].append (data) 
                data = copy.deepcopy(BassDrum['regMeasure'][patternNum][cnt+1]) 
                BassDrum['eopMeasure'][patternNum].append (data) 
            cnt += 2

    BassDrum['eosMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of Section measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eosStartBeat = Patterns[patternNum]['eosStartBeat'] 
        BassDrum['eosMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 

            if ( beatNum >= eosStartBeat ) :    # this beat will be filled in by eosFill            

                BassDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['bass'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['bass'], 'pitch': "midi." + DrumConstants.fillNotes['low']['bass'] + "_" + str(DrumConstants.fillNoteOctaves['low']['bass']) } )
                BassDrum['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['bass'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['bass'], 'pitch': "midi." + DrumConstants.fillNotes['low']['bass'] + "_" + str(DrumConstants.fillNoteOctaves['low']['bass']) } )

            else : 
                
                data = copy.deepcopy(BassDrum['regMeasure'][patternNum][cnt]) 
                BassDrum['eosMeasure'][patternNum].append (data) 
                data = copy.deepcopy(BassDrum['regMeasure'][patternNum][cnt+1]) 
                BassDrum['eosMeasure'][patternNum].append (data) 
            cnt += 2

    if ( 0 ) : 
        print ( "Bass Drum" ) 
        for patternNum in range(numPatterns) : 
            print ( "\tPattern Num: ", patternNum ) 
            for measureType in BassDrum : 
                print ( "\t\tMeasure Type: ", measureType ) 
                for item in range( 0, numBeats*2, 2 ) : 
                    print ( "Item: ", item, BassDrum[measureType][patternNum][item] ) 
                print() 

    #BassDrum => BassDrum[measureType][numPatterns][item] ) 
   

    return BassDrum



