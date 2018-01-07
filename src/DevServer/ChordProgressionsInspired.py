from __future__ import print_function

import sys
import collections
import MusicTheory

class ChordProgressionJumps : 
    
    def __init__ ( self, primaryScale ) : 
        
        self.primaryScale      = primaryScale
        self.ChordProgressions = collections.OrderedDict()        

        self.CreatePenaltyForChordProgressionJumps ( primaryScale ) 
        
    def CreatePenaltyForChordProgressionJumps ( self, homeScale )  : 

        # Chord Progression Dictionary for Inspire Mood

        self.cpDictInspire = { 
            1 : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ 1, 4, 5 ], 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' : [ 6, 3 ], 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' : [ 6, 3 ], }, 
            2 : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ 2, 1, 6 ], 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' : [ 4, 5 ], 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' : [ 4, 5 ], }, 
            3 : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ 1, 6 ], 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' : [ 4, 5 ], 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' : [ 4, 5 ], }, 
            4 : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ 1, 4, 6 ], 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' : [ 3, 5 ], 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' : [ 3, 5 ], }, 
            5 : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ 1, 5, 6 ], 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' : [ 3, 4 ], 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' : [ 3, 4 ], }, 
            6 : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ 1, 4, 5 ], 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' : [ 3 ], 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' : [ 3 ], }, 
            7 : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ 1, 6 ], 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP' : [ 4, 5 ], 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP' : [ 4, 5 ], }, 
            }

        
        self.ChordProgressions[homeScale] = collections.OrderedDict()

        for currChord in MusicTheory.AllChords : 
            self.ChordProgressions[homeScale][currChord] = {} 

            self.ChordProgressions[homeScale][currChord]['obvious'] = { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': {} }
            self.ChordProgressions[homeScale][currChord]['unusual'] = { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': {} }
            self.ChordProgressions[homeScale][currChord]['obscure'] = { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': {} }

            currChordNotes = MusicTheory.AllChords[currChord]             
            currChordHomeNote  = currChordNotes[0]


            if ( currChordHomeNote  not in MusicTheory.KeyDict[homeScale] ) : # note not found in scale. which means chord not found in scale. ignore actions for this chord and scale
                continue

            currChordHomeIndex = MusicTheory.KeyDict[homeScale][currChordHomeNote]

            if currChord.endswith ( 'Major' ) : 
                if ( MusicTheory.NoteIntensity[homeScale][currChordHomeNote] != 'Major' ) :  # major version of current chord not found in scale. only minor version found in Scale
                    continue

            elif currChord.endswith ( 'Minor' ) : 
                if ( MusicTheory.NoteIntensity[homeScale][currChordHomeNote] != 'Minor' ) : # minor version of current chord not found in scale. only major version found in Scale
                    continue
            
            elif currChord.endswith ( 'Dim' ) : 
                if ( MusicTheory.NoteIntensity[homeScale][currChordHomeNote] != 'Dim' ) : # Dim version of current chord not found in scale. only major/minor version found in Scale
                    continue
                
            else : # probbaly means 7th chords or 9th chords. ignore them
                continue

            for key in self.ChordProgressions[homeScale][currChord] :


                print ( "Key: ", key ) 

                if ( key == 'unusual' or key == 'obscure' ) :   
                    print ( "Inspire mood doesnt work yet for unusual and obscure chord progression changes" ) 
                    #sys.exit(0) 
                    continue 

                for action in self.ChordProgressions[homeScale][currChord][key] :

                    for nextChordIndex in self.cpDictInspire[currChordHomeIndex][action] : 
                        nextChordHomeNote  = MusicTheory.ReverseKeyDict[homeScale][nextChordIndex] 
                        nextChordIntensity = MusicTheory.NoteIntensity[homeScale][nextChordHomeNote] 
                        nextChord = nextChordHomeNote + nextChordIntensity
                        self.ChordProgressions[homeScale][currChord]['obvious'][action][nextChord] = {} 
                        self.ChordProgressions[homeScale][currChord]['obvious'][action][nextChord][homeScale] = ( nextChord, homeScale, 0, 0, 0, 0 ) 

                    

    def printChordProgressions ( self ) : 

        
        print ( "Primary/home scale: ", self.primaryScale ) 

        for chord in self.ChordProgressions[self.primaryScale] :
            
            print ( "\tChord: ", chord ) 

            for key in self.ChordProgressions[self.primaryScale][chord] :
                
                print ( "\t\t", key ) 
                
                for key1 in self.ChordProgressions[self.primaryScale][chord][key] :
                    
                    print ( "\t\t\t", key1 ) 

                    for key2 in self.ChordProgressions[self.primaryScale][chord][key][key1] :

                        print ( "\t\t\t\t", key2 )

                        for key3 in self.ChordProgressions[self.primaryScale][chord][key][key1][key2] :

                            print ( "\t\t\t\t\t",self.ChordProgressions[self.primaryScale][chord][key][key1][key2][key3] ) 
