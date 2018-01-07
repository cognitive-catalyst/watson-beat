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

    DrumKit = collections.OrderedDict()    

    DrumKit['regMeasure'] = collections.OrderedDict()    # this is the normal kick drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        DrumKit['regMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
    
            prob     = BeatInfo[beatNum]['kick']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['kick']['velocityMin'], BeatInfo[beatNum]['kick']['velocityMax'] )                                          
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            DrumKit['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            prob     = BeatInfo[beatNum]['snare']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['snare']['velocityMin'], BeatInfo[beatNum]['snare']['velocityMax'] )          
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            DrumKit['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )

            prob     = BeatInfo[beatNum]['hihat']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['hihat']['velocityMin'], BeatInfo[beatNum]['hihat']['velocityMax'] )  
            instrument = random.choice ( DrumConstants.hihatPieces )                                                                                                                                                                                                                                                 
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            DrumKit['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['high'][instrument], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )


            DrumKit['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
            DrumKit['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )
            DrumKit['regMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['high'][instrument], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch':"midi."+DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )




    DrumKit['lowDregMeasure'] = collections.OrderedDict()    # this is the normal kick drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        DrumKit['lowDregMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            prob     = BeatInfo[beatNum]['lowDkick']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['lowDkick']['velocityMin'], BeatInfo[beatNum]['lowDkick']['velocityMax'] )                                          
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            DrumKit['lowDregMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            prob     = BeatInfo[beatNum]['lowDsnare']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['lowDsnare']['velocityMin'], BeatInfo[beatNum]['lowDsnare']['velocityMax'] )          
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            DrumKit['lowDregMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )

            prob     = BeatInfo[beatNum]['lowDhihat']['probMax']
            randval  = random.randint ( 1, 100 ) 
            velocity = random.randint ( BeatInfo[beatNum]['lowDhihat']['velocityMin'], BeatInfo[beatNum]['lowDhihat']['velocityMax'] )  
            instrument = random.choice ( DrumConstants.hihatPieces )                                                                                                                                                                                                                                                 
            if ( not randval < int(prob) ) : 
                velocity = 0 
                                
            DrumKit['lowDregMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['high'][instrument], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch': "midi." + DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )


            DrumKit['lowDregMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
            DrumKit['lowDregMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['mid']['snare'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['mid']['snare'], 'pitch': "midi." + DrumConstants.fillNotes['mid']['snare'] + "_" + str(DrumConstants.fillNoteOctaves['mid']['snare']) } )
            DrumKit['lowDregMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['high'][instrument], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high'][instrument], 'pitch':"midi."+DrumConstants.fillNotes['high'][instrument] + "_" + str(DrumConstants.fillNoteOctaves['high'][instrument]) } )




    DrumKit['eopMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eopStartBeat = Patterns[patternNum]['eopStartBeat'] 
        DrumKit['eopMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eopStartBeat ) :    # this beat will be filled in by eopFill

                DrumKit['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                DrumKit['eopMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            else : 

                for i in range(6) : # why 6 => two events ( on and off ) per instrument ( snare, kick, hihat (3) ) =>  3*2 = 6 
                    data = copy.deepcopy(DrumKit['regMeasure'][patternNum][cnt+i]) 
                    DrumKit['eopMeasure'][patternNum].append (data) 
                cnt += 6
            

    DrumKit['eosMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of Section measure
    for patternNum in range(numPatterns) : 
        cnt = 0 
        eosStartBeat = Patterns[patternNum]['eosStartBeat'] 
        DrumKit['eosMeasure'][patternNum] = [] 
        for beatNum in range ( 1, numBeats+1 ) : 
            
            if ( beatNum >= eosStartBeat ) :    # this beat will be filled in by eosFill

                DrumKit['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )
                DrumKit['eosMeasure'][patternNum].append ( { 'beatNum': beatNum, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } )

            else : 

                for i in range(6) : # why 6 => two events ( on and off ) per instrument ( snare, kick, hihat (3) ) =>  3*2 = 6 
                    data = copy.deepcopy(DrumKit['regMeasure'][patternNum][cnt+i]) 
                    DrumKit['eosMeasure'][patternNum].append (data) 
                cnt += 6

    if ( 0 ) : 
        print ( "Drum Kit" ) 
        for patternNum in range(numPatterns) : 
            print ( "\tPattern Num: ", patternNum ) 
            for measureType in DrumKit : 
                print ( "\t\tMeasure Type: ", measureType ) 
                for item in range( len(DrumKit[measureType][patternNum]) ) : 
                    print ( "Item: ", item, DrumKit[measureType][patternNum][item] ) 

                print() 

    #sys.exit(0) 
    return DrumKit
