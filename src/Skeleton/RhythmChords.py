from __future__ import print_function
from itertools import chain

import sys
import random
import collections

import Constants
import MusicTheory


prnFlag = False

class RhythmChords () : 
    '''
    '''

    def __init__ ( self, wbLevers, scale, chord, ids, duration ) :

        self.desc = 'rhythmChords'
        self.duration  = duration
        self.homeChord = chord[0]
        self.homeScale = scale[0]

        self.speed = wbLevers['rhythmSpeed']

        # store all chord ids with same duration
        self.chordIds    = ids

        # if there is more than one chord with the same duration store them here. Will be used later to fill the actions based on the first learned chord for this duration
        self.otherChords = chord
        self.otherScales = scale
        self.octave      = 4

        self.trainedData = collections.OrderedDict() 

        if ( prnFlag ) : 
            self.PrintClassInfo() 

    def PrintClassInfo ( self ) :
        print ( )
        print ( "Layer Description: ", self.desc ) 
        print () 

    def run ( self ) : 
                                       
        chordNotes = MusicTheory.AllChords[self.homeChord]  
            
        self.maxPitch = ( MusicTheory.NotesToPitch[chordNotes[0]] + 24 ) + (self.octave*12)        
            
        if ( self.duration in Constants.OtherChordDurationBreakdown ) : 

            chordSplitDuration = []
            split = random.choice ( Constants.OtherChordDurationBreakdown[self.duration][self.speed] )
            for item in split : 
                chordSplitDuration.append ( random.choice ( Constants.MinChordDurationBreakdown[item][self.speed] ) )                 
            chordSplitDuration = list(chain.from_iterable(chordSplitDuration) )  # flatten array of arrays
                                          
        elif ( self.duration in Constants.MinChordDurationBreakdown ) : 

            chordSplitDuration = random.choice ( Constants.MinChordDurationBreakdown[self.duration][self.speed] )

        else : 
            print ( "Duration not initialized for Chord Split: ", self.duration, "\nAbort\n" ) ;
            # DurationSplit = ChordDurationForLayers.createChordDurations ( self.duration ) 
            sys.exit(0) 

        if ( 0 ) : 
            print ( "self.chordIds : ", self.chordIds )
            print ( "self.otherChords : ", self.otherChords )
            print ( "Home Pitch: ", ( MusicTheory.NotesToPitch[chordNotes[0]] + 0 ) + (self.octave*12), "Max Pitch: ", self.maxPitch ) 
            print ( "ChordNotes: ", chordNotes, "Duration: ", self.duration ) 
            print ( "chordSplitDuration: ", chordSplitDuration ) 

        newItems = [] 
        chordSplit = 0

        for item in chordSplitDuration  :             

            numNotesInChord = random.choice (  Constants.NumNotesAndClkInChordBasedOnDuration['rhythm-chords'][item] ) 

            eventItems = [] 
            unsortedItems = [] 
            pitchDict = {} 
            cumulativeStart = 0 
            midiClkStart = 0 
            midiClkEnd   = 0
            for note in range(numNotesInChord) : 

                while True : 
                    cNoteIndex = random.randint ( 0,  len(chordNotes)-1 ) 
                    cNote      = chordNotes[cNoteIndex] 
                    octave     = random.choice ( [ self.octave, self.octave + 1, self.octave + 2 ] )

                    pitch  = MusicTheory.NotesToPitch[cNote] + ( octave*12 ) 
                    if ( pitch > self.maxPitch ) : 
                        pitch -= 12
                        octave -= 1
                
                    if ( pitch not in pitchDict ) : # make sure same note does not get repeated twice
                        pitchDict[pitch] = True
                        break 
                                
                midiPitchStr = 'midi.' + cNote + "_" + str(octave) 

                velocity = random.randint ( 50, 85 ) 
                eventItems.append ( { 'action': 'StaggeredChordTonesPiano', 'notes': [cNote], 'cNoteIndex': cNoteIndex,  'midiClkStart': midiClkStart, 'midiClkEnd': midiClkEnd, 'pitch': midiPitchStr, 
                         'pitches': [pitch], 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [item], 'octaves': [octave], 'velocity': velocity } )

                cumulativeStart += midiClkStart
                midiClkStart = random.randint ( 10, 20 ) 

            
            # set end time for the first note
            midiClkEnd = item - cumulativeStart
            eventItems[0]['midiClkEnd'] = midiClkEnd
            newItems.append ( eventItems ) 

                
        if ( 0 ) : 
            for chordSplit in range(len(newItems)) : 
                print ( "ChordSplit: ", chordSplit ) 
                for item in newItems[chordSplit] :                                      
                    print ( "Rhythm Chord Item: ", item ) 
                                
        self.populateAdditionalChordsOfSameDuration ( newItems ) 


        if ( 0 ) : 
            for id in self.trainedData : 
                print() 
                print ( "Chord: ", id ) 
                for chordSplit in range(len(self.trainedData[id])) : 
                    print ( "ChordSplit: ", chordSplit ) 
                    for item in self.trainedData[id][chordSplit] : 
                        print ( "Item: ", item ) 



        return ( self.trainedData ) 


    def populateAdditionalChordsOfSameDuration ( self, items ) : 

        numChords = len(self.otherScales ) 

        #self.trainedData[self.chordIds[0]] = items



        for id in range ( numChords ) : 
            prevNote = ''
            scale    = self.otherScales[id]
            chord    = self.otherChords[id]
            chordId  = self.chordIds[id]
            newItems = [] 

            chordNotes = MusicTheory.AllChords[chord]              
            maxPitch = ( MusicTheory.NotesToPitch[chordNotes[0]] + 24 ) + (self.octave*12)        


            if ( 0 )  :
                print ( "Scale: ", scale, "Chord: ", chord, "Prev Note: ", prevNote ) 

            newItems = [] 
            for chordSplit in range(len(items)) : 

                eventItems = []
                for item in items[chordSplit] : 

                    if ( item['cNoteIndex'] <= len(chordNotes)-1 ) :                         
                        cNote  = chordNotes[item['cNoteIndex']] 
                        velocity = item['velocity']
                    else : 
                        cNote  = chordNotes[0] 
                        velocity = 0
                        
                    octave = item['octaves'][0]  #random.choice ( [ self.octave, self.octave + 1, self.octave + 2 ] )
                    pitch  = MusicTheory.NotesToPitch[cNote] + ( octave*12 ) 
                    if ( pitch > maxPitch ) : 
                        pitch -= 12
                        octave -= 1
    
                    midiPitchStr = 'midi.' + cNote + "_" + str(octave) 
                    
                    eventItems.append ( { 'event': 'on', 'action': item['action'], 'notes': [cNote], 'midiClk': item['midiClkStart'],  'pitch': midiPitchStr, 
                                          'pitches': [pitch], 'chord': chord, 'scale': scale, 'duration': item['duration'], 'octaves': [octave],  'velocity': item['velocity'] } )

                for item in items[chordSplit] : 

                    if ( item['cNoteIndex'] <= len(chordNotes)-1 ) :                         
                        cNote  = chordNotes[item['cNoteIndex']] 
                    else : 
                        cNote  = chordNotes[0] 

                    octave = item['octaves'][0]  #random.choice ( [ self.octave, self.octave + 1, self.octave + 2 ] )
                    pitch  = MusicTheory.NotesToPitch[cNote] + ( octave*12 ) 
                    if ( pitch > maxPitch ) : 
                        pitch -= 12
                        octave -= 1
    
                    midiPitchStr = 'midi.' + cNote + "_" + str(octave) 

                    eventItems.append ( { 'event': 'off', 'action': item['action'], 'notes': [cNote], 'midiClk': item['midiClkEnd'],  'pitch': midiPitchStr, 
                                          'pitches': [pitch], 'chord': chord, 'scale': scale, 'duration': item['duration'], 'octaves': [octave],  'velocity': 0 } )            

                newItems.append ( eventItems )

            self.trainedData[chordId] = newItems


        if ( 0 ) : 
            for id in range ( numChords ) : 
                chord = self.chordIds[id] 
                print() 
                print ( "Rhythm Chord: ", chord ) 
                for chordSplit in range(len(self.trainedData[chord])) : 
                    print ( "ChordSplit: ", chordSplit ) 
                    for item in self.trainedData[chord][chordSplit] : 
                        print ( "Item: ", item ) 


                        


