from __future__ import print_function

import os
import sys
import math
import random
import Constants
import collections


def createMidiEvents ( movement, uniqLayers, layerTemplateForSection ) : 

    # replicatePhraseForSections 
    MidiData = collections.OrderedDict ()
    
    for layer in uniqLayers[0] :    # the 0 indicates the first unique melody. the index 0 is needed to capture the differnt layers that have been generates ( i.e.: Bass1, Bass2, Melody, Pentatonic Melody )  
        if ( layer == 'mel5' ) : 
            for mnum in uniqLayers[0][layer]['main'] : 
                for beatnum in uniqLayers[0][layer]['main'][mnum] : 
                    print ( "\t\t\tMeasure: ", mnum, "Beat: ", beatnum, uniqLayers[0][layer]['main'][mnum][beatnum] )
                print() 



    sys.exit(0) 

    for layer in uniqLayers[0] :    # the 0 indicates the first unique melody. the index 0 is needed to capture the differnt layers that have been generates ( i.e.: Bass1, Bass2, Melody, Pentatonic Melody )  
        if ( layer == 'mel5' ) : 
            continue        
        
        MidiData[layer] = collections.OrderedDict()
            
        for sec in movement['Sections'] : 
            MidiData[layer][sec] = collections.OrderedDict()
            
            melId      = movement['Sections'][sec]['melId'] 
            repCount   = movement['Sections'][sec]['repCount'] 

            for phrase in range ( repCount ) :                 
                MidiData[layer][sec][phrase] = uniqLayers[melId][layer]

    MidiEvents = collections.OrderedDict()

    layerOctaves = { 'bass1': 3, 'bass2': 4, 'other': 3 }

    emptyEvents = [ { 'event': 'on',  'midiClk': 0, 'pitch': 'midi.C_0', 'velocity': 1 }  ] # needed for same reason as muted first section
    emptyEvents.append ( { 'event': 'off', 'midiClk': 1, 'pitch': 'midi.C_0', 'velocity': 0 } )

    CompositionSettingsForMelody = collections.OrderedDict() 

    for layer in MidiData : 
        MidiEvents[layer] = []         

        glbClk = 0 
        if layer in layerOctaves : 
            octave = layerOctaves[layer]
        else : 
            octave = layerOctaves['other']

        for sec in MidiData[layer] :             

            # begin new section event
            secStr = "# Section: " + str(sec)             
            secEvent = [ { 'event': 'comment', 'data': secStr } ]

            # meta event -  time signature             
            tse = movement['Sections'][sec]['tse']  # time signature
            tseEvent = CreateTseEvent ( tse ) 

            # meta event -  tempo
            bpm = movement['Sections'][sec]['bpm']   # Tempo
            tempoEvent = CreateTempoEvent ( bpm )            

            # mute sections based on probability
            mute = False 
            firstSectionMuted = False  # this is to record if the first section for the layer is muted or not
            # if the first section is muted, then while creating the midifile, the  midiclk does not advance past the first section. 
            # So the second section starts where the first section was supposed to start. and all the sections are moved to different places
            # this is probably a bug in python midi. 
            # to fix this bug, record if the first section is muted, and if it is, play only the first note in that section with a minimum velocity of 1.
            # this ensures that the midiclk gets pushed to the next section after muting the first section
            playProbbailityForLayerInSection = layerTemplateForSection[sec][layer]
            muteProbbailityForLayerInSection = random.randint(0, 100 ) 
            if ( muteProbbailityForLayerInSection > playProbbailityForLayerInSection ) : 
                mute = True        
                if ( sec == 1 ) : 
                    firstSectionMuted = True

            if ( layer == 'mel5' ) : 
                CompositionSettingsForMelody[sec] = collections.OrderedDict()
                if ( 1 ) : 
                    print()                 
                    MidiEvents[layer] += secEvent + tempoEvent + tseEvent 

                for phrase in MidiData[layer][sec] : 
                    CompositionSettingsForMelody[sec][phrase] = { 'clock': glbClk , 'mute': mute } 
                    if ( 1 ) : 
                        print ( "Melody Section: ", sec, " Phrase : ", phrase , " starts at global clock: ", glbClk, " Section muted: ", mute ) 

                    # begin new phrase event
                    phrStr = "# Phrase: " + str(phrase)             
                    phrEvent = [ { 'event': 'comment', 'data': phrStr } ]
                    phrEvents, currClk = CreateMidiEventsForMelody  ( MidiData[layer][sec][phrase], glbClk, mute, firstSectionMuted )  
                    phrEvents = secEvent  + tempoEvent + tseEvent + phrEvent + emptyEvents + phrEvents
                    
                    glbClk += currClk 


                    # create final MIDI File
                    foutName = "WB_Mvmt" + str(movement['id']) + "_" + layer + "_Sec" + str(sec) + "_Phrase" + str(phrase) 
                    fout = open ( foutName + ".py", mode='w' ) ;
                    #print ( "foutName ", foutName+ ".py" ) ;
                    WriteInitialMidiFileSequence ( fout ) 
                    WriteMidiEvents ( fout, phrEvents ) 
                    WriteFinalMidiFileSequence ( fout, foutName ) 


                    if ( 1 ) : 
                        debugPhrEvent, deugCnt = CreateMidiEventsForMelody  ( MidiData[layer][sec][phrase], 0, mute, firstSectionMuted )   
                        MidiEvents[layer] += phrEvent + debugPhrEvent

            elif ( layer == 'piano1' or layer == 'rhythmChords' ) : 
                MidiEvents[layer] += secEvent + tempoEvent + tseEvent 
                MidiEvents[layer] += CreateMidiEventsForRhythm ( MidiData[layer][sec], mute, firstSectionMuted ) 

            else : 
                MidiEvents[layer] += secEvent + tempoEvent + tseEvent 
                MidiEvents[layer] += CreateMidiEventsForOtherLayers ( MidiData[layer][sec], mute, firstSectionMuted, octave ) 

        if ( 1 or layer != 'mel5' ) : 
            foutName = "WB_Mvmt" + str(movement['id']) + "_" + layer 
            # create final MIDI File
            fout = open ( foutName + ".py", mode='w' ) ;
            #print ( "foutName ", foutName+ ".py" ) ;
            WriteInitialMidiFileSequence ( fout ) 
            WriteMidiEvents ( fout, MidiEvents[layer] ) 
            WriteFinalMidiFileSequence ( fout, foutName ) 


    if ( 0 ) : 
        for layer in MidiEvents : 
            if ( layer == 'mel5' ) : 
                continue
            for event in MidiEvents[layer] : 
                print ( MidiEvents[layer][event] ) 

    return CompositionSettingsForMelody


def CreateMidiEventsForMelody  ( midiData, currClk, mute, firstSectionMuted ) : 
    
    midiEvents = [] 
    localClk = 0 
    if ( currClk > 0 ) : 
        currClk -= 1

    for item in midiData :                     
        for i in range ( len(item['notes']) ) :            

            melOctave = item['pitches'][i] // 12
            pitch = 'midi.' + item['notes'][i] + "_" + str(melOctave) 

            # to fix this bug, record if the first section is mutes, and if it is, play only the first note in that section with a minimum velocity of 1.
            # this ensures that the midiclk gets pushed to the next section after muting the first section
            if ( mute ==  True and firstSectionMuted == True ) : 
                velocity = 1
                firstSectionMuted = False

            elif ( mute ==  True ) : 
                velocity = 0
            else :
                velocity = item['velocity'][i] 
                    
            midiEvents.append ( { 'event': 'on', 'midiClk': currClk, 'pitch': pitch, 'velocity': velocity }  )                         

            midiClk = item['duration'][i]            

            velocity = 0
            midiEvents.append (  { 'event': 'off', 'midiClk': midiClk, 'pitch': pitch, 'velocity': velocity }  ) 
            localClk += midiClk
            currClk = 0 

    return midiEvents, localClk
    

def CreateMidiEventsForRhythm ( midiData, mute, firstSectionMuted ) :

    midiEvents = [] 
    for phrase in midiData :
        phrStr = "# Phrase: " + str(phrase) 
        midiEvents.append (  { 'event': 'comment', 'data': phrStr }  )

        for chordSplit in midiData[phrase] : 
            for item in chordSplit : 
                
                # to fix this bug, record if the first section is mutes, and if it is, play only the first note in that section with a minimum velocity of 1.
                # this ensures that the midiclk gets pushed to the next section after muting the first section
                if ( mute ==  True and firstSectionMuted == True ) : 
                    velocity = 1
                    firstSectionMuted = False
                elif ( mute ==  True ) : 
                    velocity = 0 
                else :
                    velocity = item['velocity']
                    
                # rhythm section already has start and end midi clock. so no need for separate on off events                        
                midiEvents.append ( { 'event': item['event'], 'midiClk': item['midiClk'], 'pitch': item['pitch'], 'velocity': velocity } ) 

    return midiEvents
                

def CreateMidiEventsForOtherLayers ( midiData, mute, firstSectionMuted, octave ) :

    midiEvents = [] 
    for phrase in midiData :
        phrStr = "# Phrase: " + str(phrase) 
        midiEvents.append (  { 'event': 'comment', 'data': phrStr }  )

        for item in midiData[phrase] :                     
            for i in range ( len(item['notes']) ) :

                midiClk = 0
                pitch = 'midi.' + item['notes'][i] + "_" + str(octave) 
                # to fix this bug, record if the first section is mutes, and if it is, play only the first note in that section with a minimum velocity of 1.
                # this ensures that the midiclk gets pushed to the next section after muting the first section
                if ( mute ==  True and firstSectionMuted == True ) : 
                    velocity = 1
                    firstSectionMuted = False
                    
                    #pitch = 'midi.' + item['notes'][i] + "_" + str(0) 
                    #item['duration'][i] = 1


                elif ( mute ==  True ) : 
                    velocity = 0
                else :
                    velocity = random.randint ( 50, 85 ) 
                    
                midiEvents.append (  { 'event': 'on', 'midiClk': midiClk, 'pitch': pitch, 'velocity': velocity }  ) 
                        
                midiClk = item['duration'][i]

                velocity = 0
                midiEvents.append (  { 'event': 'off', 'midiClk': midiClk, 'pitch': pitch, 'velocity': velocity }  ) 

    return midiEvents

        


def WriteMidiEvents ( fout, data ) : 
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
            string = "time = midi.TimeSignatureEvent(tick=" + str( item['midiClk'] ) +  ", data = " + item['data'] + ")" + "\n" ; 
            fout.write ( string ) ;
            fout.write ( "track.append(time)\n" ) 
        elif ( item['event'] == 'tempo' ) :                     
            string = "tempo = midi.SetTempoEvent(tick=" + str( item['midiClk'] ) +  ", data = " + item['data'] + ")" + "\n" ; 
            fout.write ( string ) ;
            fout.write ( "track.append(tempo)\n" )                 
        elif ( item['event'] == 'comment' ) :                     
            string = item['data'] + "\n" 
            fout.write ( string ) ;
            
        
def WriteFinalMidiFileSequence ( fout, foutName ) :

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
        
    #print ( "\nOutput midi file: %s\n" %(foutMidiName) ) ;
    call = "python " + foutName + ".py"  ; 
    os.system ( call ) ;

def WriteInitialMidiFileSequence ( fout ) : 

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


def CreateTempoEvent ( bpm ) :

    tempoEvent = []
    tempoMicroSeconds = int ( 60000000 / bpm ) 
    tempoHex = hex( tempoMicroSeconds )                             
    length   = len(tempoHex)
    val = [] 
    # print ( "length: ", length ) 
    for i in range(3) : 
        string = tempoHex[length-2:length] 
        if ( string[0] == 'x' ) : 
            string = '0' + tempoHex[length-1:length]                                     
        # print ( string ) 
        length -= 2
        intString =  int(string, 16)
        val.append ( intString ) 
                        
    data = list(reversed(val))
    data = str(data)
    length = len(data) 
    data =  "(" + data [1:length-1] + ")"
    tempoEvent.append ( { 'event': 'tempo', 'midiClk': 0, 'velocity': -1, 'pitch': 0, 'data': data }  ) 

    return tempoEvent


def CreateTseEvent ( tse ) : 

    tseEvent = [] 
    tsNumerator   = Constants.TSEs[tse]['tsNumerator'] 
    tsDenominator = Constants.TSEs[tse]['tsDenominator']                             
    tsDenominatorPow =  int(math.log ( tsDenominator, 2 )) ;
    data  = "[" + str(tsNumerator) + ", " + str(tsDenominatorPow) + ", 24, 8]" 
    tseEvent.append (  { 'event': 'tse', 'midiClk': 0, 'velocity': -1, 'pitch': 0, 'data': data }  ) 

    return tseEvent
