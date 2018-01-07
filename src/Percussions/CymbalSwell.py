from __future__ import print_function
import sys
import copy
import random
import collections
import DrumConstants
from Skeleton import Constants

def run ( BeatInfo, tse, rhythmSpeed, pl ) : 
    if ( 0 ) : 
        print ( "Cymbalswell Drums" ) 

    numBeats = Constants.TSEs[tse]['num16thBeats'] 
    numPatterns = 1  # number of patterns to choose from for a normal measure that is not an eop measure or eos measure

    CymbalswellDrum = collections.OrderedDict()   

    CymbalswellDrum['regMeasure'] = collections.OrderedDict()    # this is the normal cymbalswell drum pattern for a measure that is not eos or eop 
    for patternNum in range(numPatterns) : 
        CymbalswellDrum['regMeasure'][patternNum] = [] 

                                
        velocity = random.randint ( 30, 60 ) 

        CymbalswellDrum['regMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'on',  'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )
        CymbalswellDrum['regMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'off', 'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': 0, 'midiClk': numBeats*DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )


    CymbalswellDrum['eopMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of phrase measure
    for patternNum in range(numPatterns) : 
        CymbalswellDrum['eopMeasure'][patternNum] = [] 

        velocity = random.randint ( 40, 70 ) 

        CymbalswellDrum['eopMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'on',  'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )
        CymbalswellDrum['eopMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'off', 'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': 0, 'midiClk': numBeats*DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )


    CymbalswellDrum['eosMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of Section measure
    for patternNum in range(numPatterns) : 
        CymbalswellDrum['eosMeasure'][patternNum] = [] 

        velocity = random.randint ( 70, 110 ) 

        CymbalswellDrum['eosMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'on',  'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': velocity, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )
        CymbalswellDrum['eosMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'off', 'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': 0, 'midiClk': numBeats*DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )


    CymbalswellDrum['emptyMeasure'] = collections.OrderedDict()  # this is the measure that will be the end of Section measure
    for patternNum in range(numPatterns) : 
        CymbalswellDrum['emptyMeasure'][patternNum] = [] 

        velocity = random.randint ( 70, 110 ) 

        CymbalswellDrum['emptyMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'on',  'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )
        CymbalswellDrum['emptyMeasure'][patternNum].append ( { 'beatNum': 1, 'event': 'off', 'note': DrumConstants.fillNotes['high']['cymbal'], 'velocity': 0, 'midiClk': numBeats*DrumConstants.SmallestGranularityInTicks, 'octave': DrumConstants.fillNoteOctaves['high']['cymbal'], 'pitch': "midi." + DrumConstants.fillNotes['high']['cymbal'] + "_" + str(DrumConstants.fillNoteOctaves['high']['cymbal']) } )



    if ( 0 ) : 
        print ( "Cymbalswell Drum" ) 
        for patternNum in range(numPatterns) : 
            print ( "\tPattern Num: ", patternNum ) 
            for measureType in CymbalswellDrum : 
                print ( "\t\tMeasure Type: ", measureType ) 
                for item in range( 0, 2, 2 ) : 
                    print ( "Item: ", item, CymbalswellDrum[measureType][patternNum][item] ) 
                print() 

    #CymbalswellDrum => CymbalswellDrum[measureType][numPatterns][item] ) 

    return CymbalswellDrum


