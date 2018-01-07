from __future__ import print_function
from itertools import chain

import sys
import copy
import random
import collections

import Constants
import MusicTheory

prnFlag = False

class Piano1 () : 
    '''
    '''

    def __init__ ( self, wbLevers, scale, chord, ids, duration ) :

        self.desc = 'piano1'
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
        self.trainedData['simple']  = collections.OrderedDict() 
        self.trainedData['complex'] = collections.OrderedDict() 


        if ( prnFlag ) : 
            self.PrintClassInfo() 

    def PrintClassInfo ( self ) :
        print ( )
        print ( "Layer Description: ", self.desc ) 
        print () 

    def run ( self, chordSplitDuration ) : 
         
        if  ( 0 ) :
            print ( "old chordSplitDuration: ", chordSplitDuration ) 
            
        if ( len( chordSplitDuration ) == 0 ) : # accompanying layer did not pass any chord duration. so create one

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


        chordNotes = MusicTheory.AllChords[self.homeChord]  
            
        self.maxPitch = ( MusicTheory.NotesToPitch[chordNotes[0]] + 24 ) + (self.octave*12)        


        if ( 0 ) : 
            print ( "self.chordIds : ", self.chordIds )
            print ( "self.otherChords : ", self.otherChords )
            print ( "Home Pitch: ", ( MusicTheory.NotesToPitch[chordNotes[0]] + 0 ) + (self.octave*12), "Max Pitch: ", self.maxPitch ) 
            print ( "ChordNotes: ", chordNotes, "Duration: ", self.duration ) 
            print ( "chordSplitDuration: ", chordSplitDuration ) 

        newItems = [] 
        chordSplit = 0

        for item in chordSplitDuration  :             

            numNotesInChord = random.choice (  Constants.NumNotesAndClkInChordBasedOnDuration['staggered'][item].keys() )                         

            eventItems = [] 
            unsortedItems = [] 
            for note in range(numNotesInChord) : 

                cNoteIndex = random.randint ( 0,  len(chordNotes)-1 ) 
                cNote      = chordNotes[cNoteIndex] 
                octave     = random.choice ( [ self.octave, self.octave + 1, self.octave + 2 ] )

                pitch  = MusicTheory.NotesToPitch[cNote] + ( octave*12 ) 
                if ( pitch > self.maxPitch ) : 
                    pitch -= 12
                    octave -= 1
                
                midiClkStart = Constants.NumNotesAndClkInChordBasedOnDuration['staggered'][item][numNotesInChord][note]
                midiClkEnd   = item  
                midiPitchStr = 'midi.' + cNote + "_" + str(octave) 

                for index, evItem in reversed(list(enumerate(eventItems))):
                    if pitch == evItem['pitches'][0] : 
                        eventItems[index]['midiClkEnd'] = midiClkStart-1
                        break 

                velocity = random.randint ( 50, 85 ) 
                eventItems.append ( { 'action': 'StaggeredChordTonesPiano', 'notes': [cNote], 'cNoteIndex': cNoteIndex,  'midiClkStart': midiClkStart, 'midiClkEnd': midiClkEnd, 'pitch': midiPitchStr, 
                         'pitches': [pitch], 'chord': self.homeChord, 'scale': self.homeScale, 'duration': [item], 'octaves': [octave], 'velocity': velocity } )


            newItems.append ( eventItems ) 

                
        if ( 0 ) : 
            for chordSplit in range(len(newItems)) : 
                print ( "ChordSplit: ", chordSplit ) 
                for item in newItems[chordSplit] :                                      
                    print ( "Piano Item: ", item ) 
            

        simpleItems = self.getSimpleChordRhythms ( newItems ) 

        self.populateAdditionalChordsOfSameDuration ( simpleItems, 'simple' ) 
        self.populateAdditionalChordsOfSameDuration ( newItems, 'complex' ) 


        if ( 0 ) : 
            for type in self.trainedData : 
                print() 
                print ( "Piano type: ", type ) 
                for id in self.trainedData[type] : 
                    print ( "Chord: ", id ) 
                    for chordSplit in range(len(self.trainedData[type][id])) : 
                        print ( "ChordSplit: ", chordSplit ) 
                        for item in self.trainedData[type][id][chordSplit] : 
                            print ( "Item: ", item ) 
    


        return ( self.trainedData['simple'], self.trainedData['complex'] ) 

    def populateAdditionalChordsOfSameDuration ( self, items, type ) : 

        numChords = len(self.otherScales ) 

        #self.trainedData[self.chordIds[0]] = items

        for id in range ( numChords ) : 
            prevNote = ''
            scale    = self.otherScales[id]
            chord    = self.otherChords[id]
            chordId  = self.chordIds[id]
            newItems = [] 

            chordNotes = MusicTheory.AllChords[chord]              

            if ( 0 )  :
                print ( "Scale: ", scale, "Chord: ", chord, "Prev Note: ", prevNote ) 

            newItems = [] 
            for chordSplit in range(len(items)) : 

                eventItems = []
                for item in items[chordSplit] : 

                    cNoteIndex = item['cNoteIndex'] 
                    if ( cNoteIndex > 2 ) : # this means this could be a seventh or ninth chord 
                        if ( len(chordNotes) <= 3 ) : #this is a triad, so pick another chord index
                            cNoteIndex = random.randint(0,len(chordNotes)-1) 
                    elif ( cNoteIndex == 2 ) : # this is definitely a triad 
                        if ( len(chordNotes) > 3 ) : #if current chord is a seventh or ninth, give it an option to pick seventh or ninth
                            if ( type == 'complex' ) : # for complex, definitely choose 7th or ninth
                                cNoteIndex = random.randint(3,len(chordNotes)-1) 
                            else : # for simple give it an option to choose 5th, 7th or 9th
                                cNoteIndex = random.randint(2,len(chordNotes)-1) 

                    cNote  = chordNotes[cNoteIndex] 
                    octave = item['octaves'][0]  #random.choice ( [ self.octave, self.octave + 1, self.octave + 2 ] )
                    pitch  = MusicTheory.NotesToPitch[cNote] + ( octave*12 ) 
                    if ( pitch > self.maxPitch ) : 
                        pitch -= 12
                        octave -= 1


                    #if ( pitch > maxPitch ) : 
                    #    pitch -= 12
                    #   octave -= 1
    
                    midiPitchStr = 'midi.' + cNote + "_" + str(octave) 
    

                    eventItems.append ( { 'event': 'on', 'action': item['action'], 'notes': [cNote], 'midiClkStart': item['midiClkStart'],  'pitch': midiPitchStr, 
                             'pitches': [pitch], 'chord': chord, 'scale': scale, 'duration': item['duration'], 'octaves': [octave],  'velocity': item['velocity'] } )

                    eventItems.append ( { 'event': 'off', 'action': item['action'], 'notes': [cNote], 'midiClkStart': item['midiClkEnd'],  'pitch': midiPitchStr, 
                             'pitches': [pitch], 'chord': chord, 'scale': scale, 'duration': item['duration'], 'octaves': [octave],  'velocity': 0 } )



                # sort the event items based on the intermediate midi clk for this chord split
                sortedEventItems = sorted ( eventItems, key=lambda val: val['midiClkStart'] ) 

                if ( 0 ) : 
                    print ( 'Type: ', type, 'Length of Items: ', len(items[chordSplit]) ) 
                    for item in items[chordSplit] : 
                        print ( 'Items: ', item ) 
                    print() 
                
                    print ( 'Type: ', type, 'Length of Event Items: ', len(eventItems) ) 
                    for item in eventItems : 
                        print ( 'Event Items: ', item ) 
                    print() 

                    print (  'Type: ', type, 'Length of Sorted Event Items: ', len(sortedEventItems) ) 
                    for item in sortedEventItems : 
                        print ( 'SortedEventItems:', item ) 
                    print() 

                if ( len(eventItems) > 0 ) : 
                
                    # create the midi clk for the first item # should be 0
                    sortedEventItems[0]['midiClk'] = sortedEventItems[0]['midiClkStart']
                    # create the midi clk for the rest of the items in this chord split
                    for val in range ( 1, len(sortedEventItems), 1 ) : 
                        sortedEventItems[val]['midiClk'] = sortedEventItems[val]['midiClkStart'] -  sortedEventItems[val-1]['midiClkStart']
            
                newItems.append ( sortedEventItems )
                #newItems.append ( eventItems )

            self.trainedData[type][chordId] = newItems


        if ( 0 ) : 
            print() 
            print ( "Piano Type: ", type ) 
            for id in range ( numChords ) : 
                chord = self.chordIds[id] 
                print ( "Chord: ", chord ) 
                for chordSplit in range(len(self.trainedData[type][chord])) : 
                    print ( "ChordSplit: ", chordSplit ) 
                    for item in self.trainedData[type][chord][chordSplit] : 
                        print ( "Item: ", item ) 





    def getSimpleChordRhythms ( self, newItems ) : 

        if ( 0 ) : 
            print ( "Complex Items" ) 
            for chordSplit in range(len(newItems)) : 
                print ( "ChordSplit: ", chordSplit ) 
                for item in newItems[chordSplit] :                                      
                    print ( "Piano Item: ", item ) 
            print()


        simpleItems = []
        for chordSplit in range(len(newItems)) : 
            eventItems = [] 
            for item in newItems[chordSplit] :                                      
                if ( (item['midiClkStart'] % Constants.NoteDurationDict['eighth'] == 0) and ( item['midiClkEnd'] - item['midiClkStart'] >= Constants.NoteDurationDict['eighth']-50 )  ) : # exclude all 16th notes                                        
                    if ( item['octaves'][0] > self.octave + 1 ) :  # reduce range of the notes
                        data = copy.deepcopy(item)   # deep copy to make sure the original does not change
                        data['octaves'][0] -= 1 
                        data['pitches'][0] -= 12
                        data['pitch'] = "midi." + data['notes'][0] + "_" + str(data['octaves'][0])
                        eventItems.append ( data ) 
                    else :
                        eventItems.append ( item ) 

 
                        
            simpleItems.append ( eventItems ) 

        if ( 0 ) : 
            print ( "Simple Items" ) 
            for chordSplit in range(len(simpleItems)) : 
                print ( "ChordSplit: ", chordSplit ) 
                for item in simpleItems[chordSplit] :                                      
                    print ( "Piano Item: ", item ) 
            print()

            print ( "Complex Items" ) 
            for chordSplit in range(len(newItems)) : 
                print ( "ChordSplit: ", chordSplit ) 
                for item in newItems[chordSplit] :                                      
                    print ( "Piano Item: ", item ) 
            print()


        return simpleItems
