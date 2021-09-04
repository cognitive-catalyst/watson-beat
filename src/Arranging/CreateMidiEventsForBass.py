from __future__ import print_function
import os
import sys
import random
import collections


def CreateMidiEvents ( layer, uniqCPId, secId, chId, sectionChordData, movementLayerData ) : 


    layerOctaves = { 'bass1': 3, 'bass2': 4, 'other': 3, 'bass3': 4 }

    globalStartTick = sectionChordData['globalStartTick']
    globalEndTick = sectionChordData['globalEndTick']

    midiEvents = []

    for item in movementLayerData : 

        note = item['notes'][0]

        if layer == 'mel5' : 
            octave   = item['pitches'][0] // 12 
            velocity = item['velocity'][0]
        else : 
            octave = layerOctaves[layer]
            if ( 'velocity' not in item ) : 
                velocity = random.randint ( 60, 90 )
            else : 
                velocity = item['velocity']

        midiStr = "midi." + note + "_" + str(octave) 
        duration = item['duration'][0] 

        ev = { 'event': 'on',  'startGlobalClk': globalStartTick, 'velocity': velocity, 'pitch': midiStr }
        midiEvents.append ( ev ) 
        ev = { 'event': 'off', 'startGlobalClk': globalStartTick + duration, 'velocity': velocity, 'pitch': midiStr }
        midiEvents.append ( ev ) 
        
        globalStartTick += duration

        if ( globalStartTick >= globalEndTick ) : 
            break 

    return midiEvents


def CreateMidiEventsForMelody ( layer, uniqCPId, secId, chId, sectionChordData, movementLayerData ) : 


    globalStartTick = sectionChordData['globalStartTick']
    globalEndTick = sectionChordData['globalEndTick']

    midiEventsAll = []
    midiEventsLow = []
    midiEventsMedium = []
    midiEventsHigh = []

    for item in movementLayerData : 

        note = item['notes'][0]

        octave   = item['pitches'][0] // 12 
        velocity = item['velocity'][0]

        midiStr = "midi." + note + "_" + str(octave) 
        duration = item['duration'][0] 

        if ( duration < 240 ) : 
            velocityLow = velocity
            velocityMed = 0 
            velocityHigh = 0 

        elif ( duration >= 240 and duration <= 480 ) : 
            velocityLow = 0 
            velocityMed = velocity
            velocityHigh = 0

        elif ( duration > 480 ) : 
            velocityLow = 0 
            velocityMed = 0
            velocityHigh = velocity



        ev = { 'event': 'on',  'startGlobalClk': globalStartTick, 'velocity': velocityLow, 'pitch': midiStr }
        midiEventsLow.append ( ev ) 

        ev = { 'event': 'on',  'startGlobalClk': globalStartTick, 'velocity': velocityMed, 'pitch': midiStr }
        midiEventsMedium.append ( ev ) 

        ev = { 'event': 'on',  'startGlobalClk': globalStartTick, 'velocity': velocityHigh, 'pitch': midiStr }
        midiEventsHigh.append ( ev ) 

        ev = { 'event': 'on',  'startGlobalClk': globalStartTick, 'velocity': velocity, 'pitch': midiStr }
        midiEventsAll.append ( ev ) 

        velocity = 0 
        ev = { 'event': 'off', 'startGlobalClk': globalStartTick + duration, 'velocity': velocity, 'pitch': midiStr }
        midiEventsLow.append ( ev ) 
        midiEventsMedium.append ( ev ) 
        midiEventsHigh.append ( ev ) 
        midiEventsAll.append ( ev )         

        globalStartTick += duration

        if ( globalStartTick >= globalEndTick ) : 
            break 

  
    return midiEventsLow, midiEventsMedium, midiEventsHigh, midiEventsAll



def CreateMidiEventsForPiano ( layer, uniqCPId, secId, chId, repCount, numChordsInSection, sectionChordData, movementLayerData ) : 

    globalStartTick = sectionChordData['globalStartTick']
    globalEndTick = sectionChordData['globalEndTick']

    if ( repCount == 1 ) : # make all chords simple
        type = 'simple'
    else : 
        phraseNum = ( chId // numChordsInSection ) + 1
        actualChordId = chId % numChordsInSection
        if ( phraseNum == 2 and actualChordId == numChordsInSection-1 ) : # last chord in second phrase
            type = 'complex'
        elif ( phraseNum == 3 and ( actualChordId == numChordsInSection-1 or actualChordId == 0 ) ) : # last or first chord in second phrase
            type = 'complex'
        elif ( phraseNum > 3 ) : 
            type = random.choice ( ['simple', 'complex'] ) 
        else :             
            type = 'simple'

    midiEvents = [] 

    for item in movementLayerData[type] : 
        midiStr = item['pitch']
        event = item['event']
        velocity = item['velocity']
        clk = item['midiClk'] + globalStartTick 

        if ( event == 'on' and clk >= globalEndTick ) : 
            break 
        elif ( event == 'off' and clk >= globalEndTick ) : 
            clk = globalEndTick 

        
        ev = { 'event': event,  'startGlobalClk': clk, 'velocity': velocity, 'pitch': midiStr }
        midiEvents.append ( ev ) 
        globalStartTick = clk

        #if ( globalStartTick >= globalEndTick ) : 
        #    break 

    return midiEvents 



def CreateMidiEventsForRhythmChords ( layer, uniqCPId, secId, chId, repCount, numChordsInSection, sectionChordData, movementLayerData ) : 

    globalStartTick = sectionChordData['globalStartTick']
    globalEndTick = sectionChordData['globalEndTick']

    midiEvents = [] 

    for item in movementLayerData : 


        midiStr = item['pitch']
        event = item['event']
        velocity = item['velocity']
        clk = item['midiClk'] + globalStartTick 

        if ( event == 'on' and clk >= globalEndTick ) : 
            break 
        elif ( event == 'off' and clk >= globalEndTick ) : 
            clk = globalEndTick 

        
        ev = { 'event': event,  'startGlobalClk': clk, 'velocity': velocity, 'pitch': midiStr }
        midiEvents.append ( ev ) 
        globalStartTick = clk

        #if ( globalStartTick >= globalEndTick ) : 
        #    break 

    return midiEvents 


def CreateMidiEventsForStrings ( layer, uniqCPId, secId, phId, repCount, numChordsInSection, sectionPhraseData, movementLayerData ) : 

    globalStartTick = sectionPhraseData['globalStartTick']
    globalEndTick = sectionPhraseData['globalEndTick']

    midiEvents = [] 

    for item in movementLayerData : 

        midiStr = item['pitch']
        event = item['event']
        velocity = item['velocity']
        clk = item['midiClk'] + globalStartTick 

        if ( event == 'on' and clk >= globalEndTick ) : 
            break 
        elif ( event == 'off' and clk >= globalEndTick ) : 
            clk = globalEndTick 
        
        ev = { 'event': event,  'startGlobalClk': clk, 'velocity': velocity, 'pitch': midiStr }

        if ( 0 and layer == 'leftPianoBass' ) : 
            print ( layer, phId, secId, ev ) 

        midiEvents.append ( ev ) 
        globalStartTick = clk

        #if ( globalStartTick >= globalEndTick ) : 
        #    break 

    return midiEvents 


def CreateMidiEventsForPercussions ( layer, density, uniqCPId, secId, phId, repCount, numChordsInSection, fills, sectionPhraseData, movementLayerData ) : 

    globalStartTick = sectionPhraseData['globalStartTick']
    globalEndTick = sectionPhraseData['globalEndTick']

    startMNum = sectionPhraseData['startMNum']
    endMNum   = sectionPhraseData['endMNum']
    numMeasures = endMNum - startMNum + 1

    midiEvents = [] 


    if ( density <= 7 and layer.endswith('drumsKit')) :
        regularType = 'lowDregMeasure'
    else :
        regularType = 'regMeasure'

    if ( layer == 'drumsCymbalSwell' ) : # play cymbal swell for only one measure in the phrase
        cymbalsPlayed = False

    for mnum in range ( numMeasures ) : 

        if ( not fills ) :  # if no fills for this section then use regular measures
            measureType = regularType 
        elif ( repCount == 1 ) :
            measureType = regularType 
        elif ( mnum == numMeasures-1 and phId == repCount-1 ) :  # eos
            measureType = 'eosMeasure'
        elif ( mnum == numMeasures-1 and phId%2 == 0 ) :   # end or phrase, but not eos, but not every conscutive phrase
            if ( random.randint( 0, 50 ) > 50 ) :
                measureType = regularType 
            else :
                measureType = 'eopMeasure'
        elif ( mnum == numMeasures-1 ) :   # end or phrase, but not eos
            measureType = 'eopMeasure'
        else : 
            measureType = regularType 



        if (  layer == 'drumsCymbalSwell' and cymbalsPlayed ) :   # play cymbal swell for only one measure in the phrase
            measureType = 'emptyMeasure' 

        elif ( layer == 'drumsCymbalSwell' and not cymbalsPlayed ) : 
            cymbalsPlayed = True 


        patternNumber = 0

        for item in movementLayerData[measureType][patternNumber]: 

            midiStr = item['pitch']
            event = item['event']
            velocity = item['velocity']
            clk = item['midiClk'] + globalStartTick 

            if ( event == 'on' and clk >= globalEndTick ) : 
                break 
            elif ( event == 'off' and clk >= globalEndTick ) : 
                clk = globalEndTick 
        
            ev = { 'event': event,  'startGlobalClk': clk, 'velocity': velocity, 'pitch': midiStr }

            if ( 0 and layer == 'drumsKick' ) : 
                print ( layer, phId, secId, ev ) 

            midiEvents.append ( ev ) 
            globalStartTick = clk

            # if ( globalStartTick >= globalEndTick ) : 
            #    break 

    return midiEvents 


def CreateMidiEventsForPercussionFills ( layer, uniqCPId, secId, phId, repCount, numChordsInSection, fills, sectionPhraseData, movementLayerData ) : 

    globalStartTick = sectionPhraseData['globalStartTick']
    globalEndTick = sectionPhraseData['globalEndTick']

    startMNum = sectionPhraseData['startMNum']
    endMNum   = sectionPhraseData['endMNum']
    numMeasures = endMNum - startMNum + 1

    midiEvents = [] 

    for mnum in range ( numMeasures ) : 

        if ( not fills ) :  # if no fills for this section then use regular measures
            fillType = 'eopFillsForDrums'
            measureType = 'emptyMeasure'            
        elif ( repCount == 1 ) : 
            fillType = 'eopFillsForDrums'
            measureType = 'emptyMeasure'            
        elif ( mnum == numMeasures-1 and phId == repCount-1 ) :  # eos
            fillType = 'eosFillsForDrums'
            measureType = 'fillMeasure'
        elif ( mnum == numMeasures-1 and phId%2 == 1) :   # end or phrase, but not eos, but not every conscutive phrase
            fillType = 'eopFillsForDrums'
            measureType = 'fillMeasure'
        else : 
            fillType = 'eopFillsForDrums'
            measureType = 'emptyMeasure'            

        patternNumber = 0

        for beatNum in movementLayerData[fillType][patternNumber][measureType]: 

            item = movementLayerData[fillType][patternNumber][measureType][beatNum] 

            midiStr = item['pitch']
            event = item['event']
            velocity = item['velocity']
            clk = item['midiClk'] + globalStartTick 

            if ( event == 'on' and clk >= globalEndTick ) : 
                break 
            elif ( event == 'off' and clk >= globalEndTick ) : 
                clk = globalEndTick 
        
            ev = { 'event': event,  'startGlobalClk': clk, 'velocity': velocity, 'pitch': midiStr }

            if ( 0 and layer == 'drumsKick' ) : 
                print ( layer, phId, secId, ev ) 

            midiEvents.append ( ev ) 
            globalStartTick = clk

            # if ( globalStartTick >= globalEndTick ) : 
            #    break 

    return midiEvents 





def CreateMidiFileForBass ( mvNum, secId, layer, midiEvents, outdir ) : 

    if ( 0 ) : 
        print ( "Before Sorting Layer", layer, "MvNum: ", mvNum, "Section Id: ", secId ) 
        for ev in midiEvents : 
            print ( ev ) 
        print() 


    # sort midi events based on global clock 
    sortedMidiEvents = sorted ( midiEvents, key= lambda x: x['startGlobalClk'] ) 

    if ( 0 ) : 
        print ( "After Sorting Layer", layer, "MvNum: ", mvNum, "Section Id: ", secId ) 
        for ev in sortedMidiEvents : 
            print ( ev ) 
        print() 

        
    #create local Midi clk
    initialMuteSection = [] 
    globalClk = sortedMidiEvents[0]['startGlobalClk'] 
    if ( globalClk != 0 ) :  # ie not the first section

        ev = { 'event': 'on',  'midiClk' : 0 , 'startGlobalClk': 0, 'velocity': 1, 'pitch': 'midi.C_0' } 
        initialMuteSection.append ( ev ) 
        ev = { 'event': 'off', 'midiClk':  1,  'startGlobalClk': 1, 'velocity': 0, 'pitch': 'midi.C_0' } 
        initialMuteSection.append ( ev ) 
        globalClk -= 1

    numEvents = len(sortedMidiEvents) 
    for evNum in range(numEvents) : 
        sortedMidiEvents[evNum]['midiClk'] = globalClk
        if ( evNum <= numEvents-2 ) :
            globalClk = sortedMidiEvents[evNum+1]['startGlobalClk'] - sortedMidiEvents[evNum]['startGlobalClk'] 
        
            
    if ( 0 ) : 
        print ( "After local midi clk" ) 
        for ev in sortedMidiEvents : 
            print ( ev ) 
        print() 

    foutName = outdir + "WB_Mvmt" + str(mvNum) + "_Sec" + str(secId) + "_" + layer 
    fout = open ( foutName + ".py", mode='w' ) 
    print("ouput " + foutName)
        
    
    WriteInitialMidiFileSequence ( fout ) 
    WriteMidiEvents ( fout, initialMuteSection ) 
    WriteMidiEvents ( fout, sortedMidiEvents ) 
    WriteFinalMidiFileSequence ( fout, foutName )     

    


def WriteMidiEvents (  fout, data ) : 
    for item in data  : 

        if ( item['event'] == 'on' ) : 
            string = "on = midi.NoteOnEvent(tick=" + str( item['midiClk'] ) + ", velocity=" +  str(item['velocity']) + ", pitch=" + item['pitch']  + ")" + "\n" ;
            fout.write ( string ) ;
            fout.write ( "track.append(on)\n" ) 
        elif ( item['event'] == 'off' ) : 
            string = "off = midi.NoteOffEvent(tick=" + str( item['midiClk'] ) + ", velocity=" +  str(item['velocity']) + ", pitch=" + item['pitch']  + ")" + "\n" ;
            fout.write ( string ) ;
            fout.write ( "track.append(off)\n" ) 
        elif ( item['event'] == 'tse' ) :                     
            string = "#time = midi.TimeSignatureEvent(tick=" + str( item['midiClk'] ) +  ", data = " + item['data'] + ")" + "\n" ; 
            fout.write ( string ) ;
            fout.write ( "#track.append(time)\n" ) 
        elif ( item['event'] == 'tempo' ) :                     
            string = "#tempo = midi.SetTempoEvent(tick=" + str( item['midiClk'] ) +  ", data = " + item['data'] + ")" + "\n" ; 
            fout.write ( string ) ;
            fout.write ( "#track.append(tempo)\n" )                 
        elif ( item['event'] == 'comment' ) :                     
            string = item['data'] + "\n" 
            fout.write ( string ) ;
            
        
def WriteFinalMidiFileSequence (  fout, foutName ) :

    foutMidiName = foutName + ".mid" 
    fout.write ( "\n" ) ;
    fout.write ("# Midi Events End Here" ) ;
    fout.write ("\neot = midi.EndOfTrackEvent(tick=1)" ) ;
    fout.write ("\ntrack.append(eot)" ) ;
    fout.write ( "\n# Print out the pattern" ) ;
    fout.write ( "\n#print pattern" ) ;
    # Save the pattern to disk
    fout.write ( "\nmidi.write_midifile(\"%s\", pattern)" %(foutMidiName) ) ;
    fout.close() ;
        
    print ( "\nOutput midi file: %s\n" %(foutMidiName) ) ;
    call = "python " + foutName + ".py"  ; 
    os.system ( call ) ;
    #call = "rm " + foutName + ".py"  ; 
    #os.system ( call ) ;
    

def WriteInitialMidiFileSequence (  fout ) : 

    fout.write ( "import midi\n" ) ;
    fout.write ( "# Instantiate a MIDI Pattern (contains a list of tracks)\n" ) ;
    fout.write ( "pattern = midi.Pattern(format=%d, resolution=%d)\n" %(0, 480) ) ; #tsInfo['resolution']) ) ;
    fout.write ( "# Instantiate a MIDI Track (contains a list of MIDI events)\n" ) ;
    fout.write ( "track = midi.Track()\n" ) ;
    fout.write ( "# Append the track to the pattern\n" ) ;
    fout.write ( "pattern.append(track)\n" ) ;
    fout.write ("# Midi Events Start Here" ) ;
    fout.write ( "\n" ) ;
    fout.write ("# Instantiate a MIDI note on event, append it to the track\n" ) ;
    fout.write ( "\n" ) ;
    

