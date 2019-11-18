from __future__ import print_function

import re
import os
import sys
import copy
import random
import collections
import MusicTheory

class MidiTrainingData :

    def __init__ ( self, midiDumpFile ) : 
        
        self.resolution = 0 

        self.readDumpFile ( midiDumpFile ) 
        #self.printTracks() 


        self.removeOverlaps()
        #self.printTracks() 
        #sys.exit(0) 
        
    def removeOverlaps ( self ) :

        trackName = 'melody'
        trackName = 'other'
        lastItem = len(self.Tracks[trackName][1].keys())

        for item in range(len(self.Tracks[trackName][1].keys())):
            if item in self.Tracks[trackName][1] :

                s1 = self.Tracks[trackName][1][item]['Clk'][0]
                e1 = self.Tracks[trackName][1][item]['Clk'][1]

                for nextItem in range ( item+1, lastItem, 1 ) :

                    if nextItem in self.Tracks[trackName][1] :

                        s2 = self.Tracks[trackName][1][nextItem]['Clk'][0]
                        e2 = self.Tracks[trackName][1][nextItem]['Clk'][1]

                        if ( s1 < e2 and ( (e1-s2) > 100 ) )  :
                             print ( "Overlap found between: " ,item, nextItem, self.Tracks[trackName][1][item] , self.Tracks[trackName][1][nextItem] )
                             print()
                             del self.Tracks[trackName][1][nextItem]


    def ExtractChords ( self, Chords, Scales, durations ) : 
        

        trackName = 'melody'
        trackName = 'other'
        glbClk = 0            
        chord  = 0 
        currDuration = durations[chord] 
        
        self.melody = collections.OrderedDict() 
        self.melody[chord] = [] 

        self.melodyPL = collections.OrderedDict() 
        numMelNotes = 0 


        while ( chord != len(Chords) ) : 
            for item in self.Tracks[trackName][1] : 
             
                if ( 0 ) : 
                    print ( "Item: ", self.Tracks[trackName][1][item] , "Chord: ", chord, "End Chord Duration: ", currDuration ) 
    
                # note extends to both chords. is in a chord boundary. Assume chord boundary is 1440. note starts at 1280 but ends at 1600.
                # split the note into 2. NoteA starts at 1280 , ends at 1430. Note B starts at 1440, ends at 1600
                if ( self.Tracks[trackName][1][item]['Clk'][1] > currDuration and self.Tracks[trackName][1][item]['Clk'][0] < currDuration ) :                             
                    newItemA = copy.deepcopy ( self.Tracks[trackName][1][item] )
                    newItemB = copy.deepcopy ( self.Tracks[trackName][1][item] )
    
                    newItemA['Clk'][1] = currDuration - 10   # change end of note A to 10 ticks before end of chord
                    newItemB['Clk'][0] = currDuration  # change beginning of note B to start of new chord ( or end of current chord)
    
                    newItemA['duration'] = newItemA['Clk'][1] - newItemA['Clk'][0]
                    newItemB['duration'] = newItemB['Clk'][1] - newItemB['Clk'][0]
    
                    newItemA['chord'] = Chords[chord]
                    newItemA['scale'] = Scales[chord]
    
    
                    self.melodyPL[numMelNotes] = newItemA
                    numMelNotes += 1
                    self.melody[chord].append ( newItemA ) 
    
                    chord += 1
                    if ( chord >= len(durations) ) : 
                         break
    
                    self.melody[chord] = []
                    currDuration += durations[chord]
    
                    newItemB['chord'] = Chords[chord]
                    newItemB['scale'] = Scales[chord]
    
    
                    self.melody[chord].append ( newItemB ) 
                    self.melodyPL[numMelNotes] = newItemB
                    numMelNotes += 1
    
    
                elif ( self.Tracks[trackName][1][item]['Clk'][0] >= currDuration  ) :  # this signals note is in new chord 
                    chord += 1
                    if ( chord >= len(durations) ) : 
                         break
    
                    currDuration += durations[chord]
                    self.melody[chord] = [] 
    
                    self.Tracks[trackName][1][item]['chord'] = Chords[chord]
                    self.Tracks[trackName][1][item]['scale'] = Scales[chord]
                    self.Tracks[trackName][1][item]['duration'] =  self.Tracks[trackName][1][item]['Clk'][1] - self.Tracks[trackName][1][item]['Clk'][0]
                    self.melody[chord].append ( self.Tracks[trackName][1][item] ) 
    
                    self.melodyPL[numMelNotes] = self.Tracks[trackName][1][item] 
                    numMelNotes += 1
    
    
                else :
                    self.Tracks[trackName][1][item]['chord'] = Chords[chord]
                    self.Tracks[trackName][1][item]['scale'] = Scales[chord]
                    self.Tracks[trackName][1][item]['duration'] =  self.Tracks[trackName][1][item]['Clk'][1] - self.Tracks[trackName][1][item]['Clk'][0]
                    self.melody[chord].append ( self.Tracks[trackName][1][item] ) 
    
    
                    self.melodyPL[numMelNotes] = self.Tracks[trackName][1][item] 
                    numMelNotes += 1

            chord += 1
            if ( chord >= len(Chords) ) : 
                break

            self.melody[chord] = [] 
            currDuration = durations[chord]
            



        if ( self.melodyPL[numMelNotes-1]['Clk'][1] != currDuration ) :
            self.melodyPL[numMelNotes] = copy.deepcopy (self.melodyPL[numMelNotes-1])
            self.melodyPL[numMelNotes]['Clk'][0] = self.melodyPL[numMelNotes-1]['Clk'][1]
            self.melodyPL[numMelNotes]['Clk'][1] = currDuration
            self.melodyPL[numMelNotes]['velocity'] = 0
            self.melodyPL[numMelNotes]['duration'] = self.melodyPL[numMelNotes]['Clk'][1] - self.melodyPL[numMelNotes]['Clk'][0]
            if ( chord >= len(durations) ) : 
                chord = len(durations) - 1
            #self.melody[chord].append ( self.melodyPL[numMelNotes] )


        if ( 0 ) : 
            print() 
            for chord in self.melody : 
                print ( "Chord: ", chord ) 
                for item in self.melody[chord] : 
                    print ( "Item: ", item ) 

                print() 

                #./LearnMelody.py midi_export_wb_melody_M1_M10.py.training_data 15000 midi_export_wb_melody_M1_M10 AsMajor 1 Melody midi_export_wb_bass_M1_M10 10 480 4 4



        if ( 0 ) : 
            for note in self.melodyPL : 
                print ( self.melodyPL[note] ) 
            print() 

        

    def printTracks ( self ) :


        trackName = 'melody'
        trackName = 'other'

        #for item in self.Tracks[trackName][0] : 
        #    for item1 in self.Tracks[trackName][0][item] :
        #        print ( item1, item, self.Tracks[trackName][0][item][item1] )

        #print ( "alsdjfjaskldfjlkasdjf" ) 
        #print() 

        #print ( "num tracks: ", len(self.Tracks[trackName]) ) 

        lastItem = self.Tracks[trackName][1].keys()[-1] 

        for item in range(lastItem) : 
            if item in self.Tracks[trackName][1] : 
                print (  item, self.Tracks[trackName][1][item] )




    def readDumpFile ( self, midiDumpFile ) :
        
        beginMidiExtract = False
        midiFin = open ( midiDumpFile , mode = 'r' ) 


        self.Tracks = { 'melody': [], 'guitar': [], 'drums': [], 'bass': [], 'other': [], 'pad': [] }

        for line in midiFin: 
            line = line.strip ( )

            if line.startswith("midi.Pattern") :
                split_line = re.split (r'[\s*,=]', line ) 
                for i in range(len(split_line)) :
                    if ( split_line[i] == 'resolution' ) :
                        self.resolution = int(split_line[i+1]) ;                        
                        #print ( "Resolution: " , self.resolution ) 
                        self.multiplier = float (  480.0/ self.resolution ) 
                                                
                        maxTicks = ( ( self.resolution ) / 2  ) * 13 * 8 # self.resolution/2 gives the ticks for an 8th note. multiplying by 13 gives the number of ticks for one measure when using the longest time signature. multiplying that by 8 gives us 8 measures worth of ticks.
                        break

            if line.startswith("midi.Track(") or line.startswith("[midi.Track(") :
                cnt       = 0
                tick      = 0 
                glbClk    = 0 
                diffTick  = 0                 
                firstNote = True
                trackName = 'other'
                beginMidiExtract = True
                track = collections.OrderedDict () 
                track1 = collections.OrderedDict () 
                track2 = collections.OrderedDict () 
                #print ( "Start Track", trackName ) 



            if line.startswith("midi.EndOfTrackEvent(") :
                beginMidiExtract = False
             #   self.Tracks[trackName].append ( track )             
                self.Tracks[trackName].append ( track1 )             
                self.Tracks[trackName].append ( track2 )             



                #print ( "End Track", trackName ) 
                if ( 0 and trackName == 'pad' ) : 
                    break 
                if ( 1 and trackName == 'melody' ) : 
                    break 
                
                #print() 

            if ( not beginMidiExtract ) : 
                continue


            if ( glbClk > maxTicks ) :  # no need to read more than 8 measues worth of ticks when tse=13/8
                continue

            #print ( line )     

            if re.search ( "midi.TrackNameEvent", line, re.IGNORECASE ) :
                split_line = re.split (r'[\',=]', line ) 
                #print ( split_line )
                for i in range(len(split_line)) :
                    if ( split_line[i] == ' text' ) :
                        t = split_line[i+2]                        
                        if ( ( re.search('vocal', t, re.IGNORECASE) and not re.search('back', t, re.IGNORECASE) ) or ( re.search('melody', t, re.IGNORECASE) ) ) :                         
                            trackName = 'melody'                        
                        elif re.search('bass', t, re.IGNORECASE)  : 
                            trackName = 'bass'
                        elif ( re.search('guitar', t, re.IGNORECASE) or re.search('gtr', t, re.IGNORECASE) ) :
                            trackName = 'guitar'
                        elif ( re.search('drum', t, re.IGNORECASE) ) : 
                            trackName = 'drums'
                        elif ( re.search('warm pad', t, re.IGNORECASE) ) : 
                            trackName = 'pad'

                        #print ( "TrackName: ", trackName ) 

                        break 
                
    
            if ( (re.search ( "midi.NoteOnEvent", line ) ) or (re.search ( "midi.NoteOffEvent", line )) )  :
                split_line = re.split ( r'[,=\[\]\s*(]', line ) ;
       
                for i in range(len(split_line)) :                                            
                    if ( split_line[i] == 'tick' ) :
                        tick = int(split_line[i+1]) ;
                    if ( split_line[i] == 'data' ) :
                        pitch = int(split_line[i+2]) ;
                        if ( (re.search ( "midi.NoteOffEvent", line )) )  :
                            event = 'off'
                            velocity = 0 ;                            
                        elif ( (re.search ( "midi.NoteOnEvent", line )) and int(split_line[i+4]) == 0  )  :
                            event = 'off'
                            velocity = 0 
                        else:
                            event = 'on'
                            velocity = int(split_line[i+4]) ;
                        break ;
                    
                div = pitch / 12
                mod = pitch % 12
                noteStr = MusicTheory.pitchToNotes[mod] + "_" + str(div-2)             

                if ( firstNote ) : 
                    tick      = 0            
                    glbClk    = 0
                    diffTick  = 0
                    firstNote = False

                tick += diffTick
                glbClk += tick 

                #track[cnt] = { 'event': event, 'note': noteStr, 'velocity': velocity, 'tick': tick, 'pitch': pitch, 'glbTick': glbClk }                

                if ( pitch in track1 ) : 
                    lastEvent = track1[pitch].keys()[-1]  
                    numEvents = len(track1[pitch][lastEvent])

                    #print ( "Next time: ", "pitch: ", pitch, "last cnt: ", lastEvent, "even or odd, numEvents: ", numEvents , "event: ", event, track1[pitch][lastEvent] ) 

                    if ( numEvents%2 == 0 and event == 'on' )   : 
                        track1[pitch][cnt] =  [ int(glbClk*self.multiplier) ]
                        #print ( "1. Event: on: " ) 
                    elif ( numEvents%2 == 1 and event == 'off' )  : 

                        if ( int(glbClk*self.multiplier) - track1[pitch][lastEvent][-1] != 0 ) : 
                            track1[pitch][lastEvent].append ( int(glbClk*self.multiplier) ) 
                            track2[lastEvent] = { 'pitch': pitch, 'Clk': track1[pitch][lastEvent], 'velocity': random.randint ( 50, 80 ) } 
                        #print ( "2. Event: off: ", track2[lastEvent], lastEvent ) 
                        #print() 
                    elif ( numEvents%2 == 1 and event == 'on' )  : 
                        track1[pitch][cnt] =  [ int(glbClk*self.multiplier) ]


                else :                     
                    track1[pitch] = collections.OrderedDict() 
                    track1[pitch][cnt] = [ int(glbClk*self.multiplier) ]
                    #print ( "First Time: ", "pitch: ", pitch, "cnt: ", cnt, track1[pitch][cnt] ) 

                        

                cnt += 1
                diffTick = 0 
    
            elif ( re.search ( "tick=", line ) ) :                
                split_line = re.split ( r'[,=\[\]\s*(]', line ) ;
                for i in range(len(split_line)) :                                            
                    if ( split_line[i] == 'tick' ) :          
                        diffTick += int(split_line[i+1])    
                        break ;
    
            #print ( "4 glbClk : ", glbClk, "tick: ", tick, 'diffTick: ', diffTick )     
    
        midiFin.close() 
                        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
