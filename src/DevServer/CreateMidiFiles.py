from __future__ import print_function

import os
import sys
import math
import random
import Constants
import collections


class Midi : 
    def __init__ ( self, movement, uniqLayers, layerTemplateForSections ) : 

        self.movement   = movement
        self.uniqLayers = uniqLayers
        self.layerTemplateForSections = layerTemplateForSections 
        numMelodyFills = len(self.uniqLayers[0]['mel5']) 
        self.melodyFillKeys = [ "alt"+str(i) for i in range ( 1, numMelodyFills, 1 ) ] 
        #print ( self.melodyFillKeys ) 


    def ReplicateLayers ( self ) : 
        
        self.MidiData = collections.OrderedDict ()

        for layer in self.uniqLayers[0] :    # the 0 indicates the first unique melody. the index 0 is needed to capture the differnt layers that have been generates ( i.e.: Bass1, Bass2, Melody, Pentatonic Melody )  

            self.MidiData[layer] = collections.OrderedDict()

            for sec in self.movement['Sections'] : 

                pl         = self.movement['Sections'][sec]['phraseLength'] 
                melId      = self.movement['Sections'][sec]['melId'] 
                repCount   = self.movement['Sections'][sec]['repCount'] 
                self.MidiData[layer][sec] = collections.OrderedDict()

                if ( layer == 'mel5' ) : 
                    self.MidiData[layer][sec] = self.ReplicateMeasuresForMelodyUsingFills ( melId, repCount )

                elif ( layer.startswith('drums') ) : 
                    self.MidiData[layer][sec] = self.ReplicateMeasuresForPercussions ( melId, repCount, pl, layer )

                elif ( layer.startswith('fillsForDrums') ) : 
                    self.MidiData[layer][sec] = self.ReplicateMeasuresForPercussionFills ( melId, repCount, pl, layer )


                elif ( layer.startswith('piano1') ) : 
                    for phrase in range ( repCount ) :                 
                        self.MidiData[layer][sec][phrase] = self.ReplicateMeasuresForRhythmPiano ( melId,  phrase, layer )

                else : 
                    for phrase in range ( repCount ) :                 
                        self.MidiData[layer][sec][phrase] = self.uniqLayers[melId][layer]


        return ( self.CreateMidiForLayers () )

    def ReplicateMeasuresForRhythmPiano ( self, melId, phrase, layer ) : 
        
        midiData = collections.OrderedDict()
        numChordSplits = len(self.uniqLayers[melId][layer]['simple'])
        complexChordSplits = {}

        if ( phrase == 0 ) : 
            complexChordSplits = { numChordSplits-1: True } 
        elif ( phrase == 1 ) : # all odd chord splits are complex
            for i in range(1, numChordSplits, 4) : 
                complexChordSplits[i] = True 
        elif ( phrase == 3 ) : # all even chord splits are complex
            for i in range(1, numChordSplits, 2) : 
                complexChordSplits[i] = True 
        else :  # random chord splits are complex
            for i in range(numChordSplits) : 
                if ( random.randint( 1, 100 ) > 50 ) : 
                    complexChordSplits[i] = True 

        if ( 0 ) : 
            print ( "Phrase: ", phrase, "melId: ", melId, "layer: ", layer, "complexChordSplits: ", complexChordSplits ) 

        for chordSplit in range(numChordSplits) : 
            if ( chordSplit in complexChordSplits ) :  
                type = 'complex'
            else :
                type = 'simple' 
            midiData[chordSplit] = []
            for item in self.uniqLayers[melId][layer][type][chordSplit] :
                midiData[chordSplit].append ( item ) 


               
        return ( midiData ) 



    def ReplicateMeasuresForMelodyUsingFills ( self, melId, repCount ) : 
                
        melMidiData = collections.OrderedDict()
        for rep in range(repCount) : 

            melMidiData[rep] = collections.OrderedDict()

            # pick Mnum that has the fills
            mnumWithFill = random.choice ( self.uniqLayers[melId]['mel5']['main'].keys() ) 

            for mnum in self.uniqLayers[melId]['mel5']['main'] : 

                if ( rep != 0 and  mnum == mnumWithFill ) : 
                    fillKey = random.choice ( self.melodyFillKeys ) 
                    melMidiData[rep][mnum] = self.uniqLayers[melId]['mel5'][fillKey][mnum]
                else : 
                    melMidiData[rep][mnum] = self.uniqLayers[melId]['mel5']['main'][mnum]

        if ( 0 ) : 
            for rep in range(repCount) : 
                print ( "Phrase: ", rep ) 
                for mnum in melMidiData[rep] : 
                    for beatnum in melMidiData[rep][mnum] : 
                        print ( "\t\t\tMeasure: ", mnum, "Beat: ", beatnum, melMidiData[rep][mnum][beatnum] )
                print() 
                
        return melMidiData

    def ReplicateMeasuresForPercussions ( self, melId, repCount, pl, layer ) : 
                
        midiData = collections.OrderedDict()
        if ( layer == 'drumsCymbalSwell' ) : 
            for phrase in range(repCount) : 
                midiData[phrase] = collections.OrderedDict()

                for mnum in range(pl) : 
                    if ( phrase == repCount-1 and mnum >= pl-1 ) : # if it is the last phrase in the rep count and the second last measure, then cymbal swell should start
                        continue                    
                    midiData[phrase][mnum] = self.uniqLayers[melId][layer][pl]  # all other phrases and measures are empty
                if ( phrase == repCount-1 ) : # last phrase in rep count 
                    midiData[phrase][pl-1] = self.uniqLayers[melId][layer][pl-1]    # cymbal swell starts at second last measure                
        else : 
            for phrase in range(repCount) : 
                midiData[phrase] = collections.OrderedDict()
                if ( phrase == repCount -1 ) :  # last phrase in rep count
                    for mnum in range(pl-1) : 
                        midiData[phrase][mnum] = self.uniqLayers[melId][layer][mnum]            
                    midiData[phrase][pl-1] = self.uniqLayers[melId][layer][pl]  # end of section measure is empty
                else : 
                    for mnum in range(pl) : 
                        midiData[phrase][mnum] = self.uniqLayers[melId][layer][mnum]



        if ( 0 ) : 
            if ( layer == 'drumsCymbalSwell' ) :                
                for rep in range(repCount) : 
                    print ( "Phrase: ", rep ) 
                    for mnum in midiData[rep] : 
                        for item in midiData[rep][mnum] : 
                            print ( "\t\t\tMeasure: ", mnum, "Item: ", item ) 
                    print() 
                        
        return midiData


    def ReplicateMeasuresForPercussionFills ( self, melId, repCount, pl, layer ) : 
        
        midiData = collections.OrderedDict()
        for phrase in range(repCount) : 
            midiData[phrase] = collections.OrderedDict()
            if ( phrase == repCount-1 ) : # end of section 

                for mnum in range(pl-1) : 
                    midiData[phrase][mnum] = self.uniqLayers[melId][layer]['eos'][0]  # empty measure
                eosChoice = random.randint ( 1, len(self.uniqLayers[melId][layer]['eos'])-1 ) 
                midiData[phrase][pl-1] = self.uniqLayers[melId][layer]['eos'][eosChoice]  # end of section fill 

            else : 
                
                for mnum in range(pl-1) : 
                    midiData[phrase][mnum] = self.uniqLayers[melId][layer]['eop'][0]  # empty measure
                eopChoice = random.randint ( 1, len(self.uniqLayers[melId][layer]['eop'])-1 ) 
                midiData[phrase][pl-1] = self.uniqLayers[melId][layer]['eop'][eopChoice]  # end of phrase fill 

        if ( 0 ) : 
            for rep in range(repCount) : 
                print ( "Phrase: ", rep ) 
                for mnum in midiData[rep] : 
                    for item in midiData[rep][mnum] : 
                        print ( "\t\t\tMeasure: ", mnum, "Item: ", midiData[rep][mnum][item]  ) 
                print() 
              
        return midiData




    def CreateMidiForLayers ( self ) : 
        
        self.MidiEvents = collections.OrderedDict()
        CompositionSettingsForMelody = collections.OrderedDict() 
        
        layerOctaves = { 'bass1': 3, 'bass2': 4, 'other': 3 }
    
        emptyEvents = [ { 'event': 'on',  'midiClk': 0, 'pitch': 'midi.C_0', 'velocity': 1 }  ] # needed for same reason as muted first section
        emptyEvents.append ( { 'event': 'off', 'midiClk': 1, 'pitch': 'midi.C_0', 'velocity': 0 } )

        for layer in self.MidiData : 

            if ( layer != 'fillsForDrums' ) : 
                self.MidiEvents[layer] = []         

            glbClk = 0 
            if layer in layerOctaves : 
                octave = layerOctaves[layer]
            else : 
                octave = layerOctaves['other']

            for sec in self.MidiData[layer] :             
    
                # begin new section event
                secStr = "# Section: " + str(sec)             
                secEvent = [ { 'event': 'comment', 'data': secStr } ]
    
                # meta event -  time signature             
                tse = self.movement['Sections'][sec]['tse']  # time signature
                tseEvent = self.CreateTseEvent ( tse ) 
    
                # meta event -  tempo
                bpm = self.movement['Sections'][sec]['bpm']   # Tempo
                tempoEvent = self.CreateTempoEvent ( bpm )            
    
                # add section beginning comment, tempo and tse for section
                self.MidiEvents[layer] += secEvent + tempoEvent + tseEvent 

                # mute sections based on probability
                mute = False 
                firstSectionMuted = False  # this is to record if the first section for the layer is muted or not
                # if the first section is muted, then while creating the midifile, the  midiclk does not advance past the first section. 
                # So the second section starts where the first section was supposed to start. and all the sections are moved to different places
                # this is probably a bug in python midi. 
                # to fix this bug, record if the first section is muted, and if it is, play only the first note in that section with a minimum velocity of 1.
                # this ensures that the midiclk gets pushed to the next section after muting the first section
                if ( layer.startswith ( 'strings2' ) ) : 
                    playProbbailityForLayerInSection = self.layerTemplateForSections[sec]['strings2']
                elif ( layer.startswith ( 'drums' ) or layer.startswith ( 'fillsForDrums' ) ) : 
                    playProbbailityForLayerInSection = self.layerTemplateForSections[sec]['drums']
                else : 
                    playProbbailityForLayerInSection = self.layerTemplateForSections[sec][layer]
                muteProbbailityForLayerInSection = random.randint(0, 100 ) 

                if ( muteProbbailityForLayerInSection > playProbbailityForLayerInSection ) : 
                    mute = True        
                    if ( sec == 1 ) : 
                        firstSectionMuted = True
    
                if ( layer == 'mel5' ) : 
                    CompositionSettingsForMelody[sec] = collections.OrderedDict()
    
                    for phrase in self.MidiData[layer][sec] : 

                        CompositionSettingsForMelody[sec][phrase] = { 'clock': glbClk , 'mute': mute } 
                        if ( 1 ) : 
                            print ( "Melody Section: ", sec, " Phrase : ", phrase , " starts at global clock: ", glbClk, " Section muted: ", mute ) 
    
                        # begin new phrase event
                        phrStr = "# Phrase: " + str(phrase)             
                        phrEvent = [ { 'event': 'comment', 'data': phrStr } ]
                        phrEvents, currClk, maxPitch, minPitch = self.CreateMidiEventsForMelody  ( self.MidiData[layer][sec][phrase], glbClk, mute, firstSectionMuted )  
                        phrEvents = secEvent  + tempoEvent + tseEvent + phrEvent + emptyEvents + phrEvents
                        CompositionSettingsForMelody[sec][phrase]['maxPitch'] = maxPitch 
                        CompositionSettingsForMelody[sec][phrase]['minPitch'] = minPitch 
                        glbClk += currClk 
        
                        # create final MIDI File
                        foutName = "WB_Mvmt" + str(self.movement['id']) + "_" + layer + "_Sec" + str(sec) + "_Phrase" + str(phrase) 
                        fout = open ( foutName + ".py", mode='w' ) ;
                        #print ( "foutName ", foutName+ ".py" ) ;
                        self.WriteInitialMidiFileSequence ( fout ) 
                        self.WriteMidiEvents ( fout, phrEvents ) 
                        self.WriteFinalMidiFileSequence ( fout, foutName )     
    
                        if ( 1 ) : 
                            debugPhrEvent, deugCnt, maxPitch, minPitch = self.CreateMidiEventsForMelody  ( self.MidiData[layer][sec][phrase], 0, mute, firstSectionMuted )   
                            self.MidiEvents[layer] += phrEvent + debugPhrEvent
    
                elif ( layer == 'piano1' or layer == 'rhythmChords' or layer == 'strings1' or layer.startswith('strings2') ) : 
                    self.MidiEvents[layer] += self.CreateMidiEventsForRhythm ( self.MidiData[layer][sec], mute, firstSectionMuted ) 

                elif (  layer.startswith('drums')) : 
                    self.MidiEvents[layer] += self.CreateMidiEventsForPercussions ( self.MidiData[layer][sec], mute, firstSectionMuted ) 
                    if ( layer == 'drumsKick' ) : 
                        if ( 'fillsForDrums' not in self.MidiEvents ) : 
                            self.MidiEvents['fillsForDrums'] = [] 
                        self.MidiEvents['fillsForDrums'] += self.CreateMidiEventsForPercussionFills ( self.MidiData['fillsForDrums'][sec], mute, firstSectionMuted ) 
    
                elif ( not layer.startswith ( 'fillsForDrums') ) : 
                    self.MidiEvents[layer] += self.CreateMidiEventsForOtherLayers ( self.MidiData[layer][sec], mute, firstSectionMuted, octave ) 
    

            if ( 1 or layer != 'mel5' ) : 
                foutName = "WB_Mvmt" + str(self.movement['id']) + "_" + layer 
                # create final MIDI File
                fout = open ( foutName + ".py", mode='w' ) ;
                #print ( "foutName ", foutName+ ".py" ) ;
                self.WriteInitialMidiFileSequence ( fout ) 
                self.WriteMidiEvents ( fout, self.MidiEvents[layer] ) 
                self.WriteFinalMidiFileSequence ( fout, foutName ) 

    

        return CompositionSettingsForMelody
    

    def CreateMidiEventsForMelody  ( self, midiData, glbClk, mute, firstSectionMuted ) : 
        
        midiEvents = [] 
        localClk   = 0 
        endTick    = 0

        if ( glbClk != 0 ) : 
            localClk = glbClk - 1
            midiEvents.append ( { 'event': 'on',  'midiClk': 0, 'pitch': 'midi.C_0', 'velocity': 1 } ) # needed for same reason as muted first section
            midiEvents.append ( { 'event': 'off', 'midiClk': 1, 'pitch': 'midi.C_0', 'velocity': 0 } )

        maxPitch = -1 
        minPitch = 100

        for mnum in midiData : 
          
            for beatnum in midiData[mnum] : 
    
                if ( midiData[mnum][beatnum]['pitch'] > maxPitch ) : 
                    maxPitch = midiData[mnum][beatnum]['pitch']

                if ( midiData[mnum][beatnum]['pitch'] < minPitch ) : 
                    minPitch = midiData[mnum][beatnum]['pitch']
                
                melOctave = midiData[mnum][beatnum]['pitch'] // 12
                pitch = 'midi.' +  midiData[mnum][beatnum]['note'] + "_" + str(melOctave) 
    
                localClk += midiData[mnum][beatnum]['startTick'] - endTick

                # to fix this bug, record if the first section is mutes, and if it is, play only the first note in that section with a minimum velocity of 1.
                # this ensures that the midiclk gets pushed to the next section after muting the first section
                if ( mute ==  True and firstSectionMuted == True ) : 
                    velocity = 1
                    firstSectionMuted = False
    
                elif ( mute ==  True ) : 
                    velocity = 0
                else :
                    velocity =  midiData[mnum][beatnum]['velocity'] 
                    
                midiEvents.append ( { 'event': 'on', 'midiClk': localClk, 'pitch': pitch, 'velocity': velocity }  )                         
                
                midiClk = midiData[mnum][beatnum]['duration']  
    
                velocity = 0
                midiEvents.append (  { 'event': 'off', 'midiClk': midiClk, 'pitch': pitch, 'velocity': velocity }  ) 
                endTick = midiData[mnum][beatnum]['endTick']
                localClk = 0
    
        localClk = endTick
        return midiEvents, localClk, maxPitch, minPitch
    
    
        
    def WriteMidiEvents ( self, fout, data ) : 
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
                
            
    def WriteFinalMidiFileSequence ( self, fout, foutName ) :
    
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
    
    def WriteInitialMidiFileSequence ( self, fout ) : 
    
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
    
    
    def CreateTempoEvent ( self, bpm ) :
    
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
    
    
    def CreateTseEvent ( self, tse ) : 
    
        tseEvent = [] 
        tsNumerator   = Constants.TSEs[tse]['tsNumerator'] 
        tsDenominator = Constants.TSEs[tse]['tsDenominator']                             
        tsDenominatorPow =  int(math.log ( tsDenominator, 2 )) ;
        data  = "[" + str(tsNumerator) + ", " + str(tsDenominatorPow) + ", 24, 8]" 
        tseEvent.append (  { 'event': 'tse', 'midiClk': 0, 'velocity': -1, 'pitch': 0, 'data': data }  ) 
    
        return tseEvent
    

    def CreateMidiEventsForPercussions ( self, midiData, mute, firstSectionMuted ) :
    
        midiEvents = [] 
        for phrase in midiData :
            phrStr = "# Phrase: " + str(phrase) 
            midiEvents.append (  { 'event': 'comment', 'data': phrStr }  )
    
            for mnum in midiData[phrase] : 

                for item in midiData[phrase][mnum] :
                
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
    
        #sys.exit(0) 

        return midiEvents

    def CreateMidiEventsForPercussionFills ( self, midiData, mute, firstSectionMuted ) :
    
        midiEvents = [] 
        for phrase in midiData :
            phrStr = "# Phrase: " + str(phrase) 
            midiEvents.append (  { 'event': 'comment', 'data': phrStr }  )
    
            for mnum in midiData[phrase] : 

                for data in midiData[phrase][mnum] :
                
                    item = midiData[phrase][mnum][data]
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
    
        #sys.exit(0) 

        return midiEvents


                
    def CreateMidiEventsForRhythm ( self, midiData, mute, firstSectionMuted ) :
    
        midiEvents = [] 
        for phrase in midiData :
            phrStr = "# Phrase: " + str(phrase) 
            midiEvents.append (  { 'event': 'comment', 'data': phrStr }  )
    
            for chordSplit in midiData[phrase] : 

                if isinstance(chordSplit, int):  # only for piano
                    chordSplit = midiData[phrase][chordSplit]

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
    
        #sys.exit(0) 

        return midiEvents
                    
    
    def CreateMidiEventsForOtherLayers ( self, midiData, mute, firstSectionMuted, octave ) :
    
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
    
    
    
    
    
    
    
    
    
    
    
