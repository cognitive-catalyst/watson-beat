from __future__ import print_function

import sys
import random
import collections

import Constants
import MidiOutput
import MusicTheory



prnFlag = True

class PMelody ( ) : 
    '''

    '''

    def __init__ ( self, wbLevers, scale, chord, ids, duration ) :

        self.desc = 'pentatonicMelody' 
        self.duration  = duration
        self.homeChord = chord[0]
        self.homeScale = scale[0]

        self.speed = wbLevers['rhythmSpeed']

        # store all chord ids with same duration
        self.chordIds    = ids

        # if there is more than one chord with the same duration store them here. Will be used later to fill the actions based on the first learned chord for this duration
        self.otherChords = chord
        self.otherScales = scale

        self.trainedData = collections.OrderedDict() 

        if ( prnFlag ) : 
            self.PrintClassInfo() 

    def PrintClassInfo ( self ) :
        print ( )
        print ( "Layer Description: ", self.desc ) 
        print () 


    def run ( self ) : 

        chosenItems = [] 

        currentOctave = 5
        prevNote = random.choice ( MusicTheory.PentatonicScale[self.homeScale] ) 
        usedTicks = 0 
        remainingTicks = self.duration - usedTicks
        
        while usedTicks < self.duration :  
            
            if ( self.homeChord.endswith ( 'Dim' ) ) :                 
                chosenNote = [ random.choice ( MusicTheory.AllChords[self.homeChord] ) ]
            else : 
                chosenNote = [ random.choice ( MusicTheory.PentatonicScale[self.homeScale] ) ]
            chosenDuration, chosenNote, totalDuration = self.getDuration ( chosenNote, remainingTicks ) 
            pitch = self.getOctavesAndPitchData ( chosenNote, prevNote, currentOctave )
            chosenData     = { 'action': 'Pentatonic', 'notes':  chosenNote, 'pitches': pitch, 'chord': self.homeChord, 'scale': self.homeScale, 'duration': chosenDuration, 'totalDuration': totalDuration } 

            usedTicks += chosenData['totalDuration']
            remainingTicks = self.duration - usedTicks
            chosenItems.append ( chosenData )
            currentOctave = chosenData['pitches'][-1]//12
            prevNote = chosenNote[-1]

            if ( 0 ) :
                print ( "Used Ticks: ", usedTicks, "remaining duration: ", remainingTicks, "Total Ticks: ", self.duration )

        if ( 1 ) : 
            for i in range(len(chosenItems)) : 
                print ( "Item: ",  chosenItems[i]) 
            print() 

        self.populateAdditionalChordsOfSameDuration ( chosenItems ) 
        return ( self.trainedData ) 


    def getDuration ( self, notes, remainingDuration ) : 
        numNotes = 1  # why one, beacuse of pentatonic
        
        while ( True ) : 
            noteLength    = random.choice ( Constants.DurationBreakdown[self.speed]['DurationProbsForNotes'][numNotes] ) 
            totalDuration = Constants.DurationBreakdown[self.speed][numNotes][noteLength]['total'] 
            if ( totalDuration <= remainingDuration ) : 
                break 

        duration = random.choice ( Constants.DurationBreakdown[self.speed][numNotes][noteLength]['choices'] ) 

        numNotes = len(duration) 
        newNotes = [] 
        for i in range ( numNotes ) : 
            newNotes.append( notes[0] ) 

        # sanity check . FIX ME. remove this check for speed
        if ( len(newNotes) != len(duration) ) : 
            print()
            print ( "Notes and Durations do not match" ) 
            print ( "Notes: ", newNotes, len(newNotes) ) 
            print ( "Duration: ", duration, len(duration) )
            print ( "Abort\n" ) 
            sys.exit(0) 

        # assign pitch information for new notes      
        return  duration, newNotes, totalDuration

    def getOctavesAndPitchData ( self, notes, prevNote, octave ) : 

        pitch = [] 
        prevNoteIndex = MusicTheory.NotesToPitch[prevNote] 
        for currNote in notes :
            currNoteIndex = MusicTheory.NotesToPitch[currNote] 

            if ( prevNoteIndex - currNoteIndex >= 7 ) : 
                octave += 1
            elif ( prevNoteIndex - currNoteIndex <= -7 ) : 
                octave -= 1

            currNotePitch = currNoteIndex + ( octave * 12 ) 
            prevNote      = currNote
            prevNoteIndex = MusicTheory.NotesToPitch[prevNote] 
            pitch.append ( currNotePitch ) 
        return pitch
        #return pitch, octave

    def populateAdditionalChordsOfSameDuration ( self, items ) : 

        numChords = len(self.otherScales ) 
        self.trainedData[self.chordIds[0]] = items

        for id in range ( 1, numChords, 1 ) : 
            prevNote = ''
            scale    = self.otherScales[id]
            chord    = self.otherChords[id]
            chordId  = self.chordIds[id]
            newItems = [] 

            if ( 1 )  :
                print ( "Scale: ", scale, "Chord: ", chord, "Prev Note: ", prevNote ) 
            for item in items : 
                action    = item['action'] 
                notes     = item['notes'] 
                duration  = item['duration']
                nextNote = random.choice ( MusicTheory.PentatonicScale[scale] ) 

                if ( 1 )  :
                    print ( "Action: ", action, "Notes: ", notes, "New Notes for chord: ", nextNote  ) 

                numNotes = len(duration) 
                newNotes = [] 
                for i in range ( numNotes ) : 
                    newNotes.append( nextNote ) 
                    
                pitch = [] 
                if ( 1 )  :
                    print ( "Action: ", action, "Notes: ", notes, "New Notes for chord: ", newNotes  ) 
                    print() 

                newItem  = { 'action': 'Pentatonic', 'notes':  newNotes, 'pitches': pitch, 'chord': chord, 'scale': scale, 'duration': duration } 
                newItems.append ( newItem ) 
                prevNote = newNotes[-1]
                if ( 1 )  :
                    print ( "Scale: ", scale, "Chord: ", chord, "Prev Note: ", prevNote ) 

            self.trainedData[chordId] = newItems

        if ( 1 ) : 
            for chId in self.trainedData : 
                print ( "Chord Id: ", chId ) 
                for item in self.trainedData[chId] : 
                    print ( item ) 
                print()
                
