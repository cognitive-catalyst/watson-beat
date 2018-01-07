from __future__ import print_function

import sys
import collections
import MusicTheory

class ChordProgressionJumps : 
    
    def __init__ ( self, primaryScale ) : 
        
        self.primaryScale      = primaryScale
        self.ChordProgressions = collections.OrderedDict()        

        self.CreatePenaltyForChordProgressionJumps ( primaryScale ) 
        

    def CreatePenaltyForChordProgressionJumps ( self, homeScale ) :

        maxPenalty = 100
        minPenalty = -100

        penaltyFreqDict = collections.OrderedDict() 
        cnt = 0 
        for currChord in MusicTheory.AllChords : 

            currScale = MusicTheory.ChordsToScale[currChord][0]  
            notesInCurrScale = MusicTheory.NotesInScale[currScale]            

            currChordNotes = MusicTheory.AllChords[currChord] 
            homeIndex = MusicTheory.NotesToPitch[currChordNotes[0]]
            pullToHome = [ MusicTheory.pitchToNotes[(homeIndex+1)%12], MusicTheory.pitchToNotes[(homeIndex+11)%12] ] 
        
            note1Index  = MusicTheory.NotesToPitch[currChordNotes[1]]
            pullToNote1 = [ MusicTheory.pitchToNotes[(note1Index+1)%12], MusicTheory.pitchToNotes[(note1Index+11)%12] ] 
        
            note2Index  = MusicTheory.NotesToPitch[currChordNotes[2]]
            pullToNote2 = [ MusicTheory.pitchToNotes[(note2Index+1)%12], MusicTheory.pitchToNotes[(note2Index+11)%12] ] 


            SeventhChord = False
            NinthChord = False
            if ( len(currChordNotes) >= 4 ) : 
                SeventhChord = True 
                note3Index  = MusicTheory.NotesToPitch[currChordNotes[3]]
                pullToNote3 = [ MusicTheory.pitchToNotes[(note3Index+1)%12], MusicTheory.pitchToNotes[(note3Index+11)%12] ] 

            if ( len(currChordNotes) >= 5 ) : 
                NinthChord = True 
                note4Index  = MusicTheory.NotesToPitch[currChordNotes[4]]
                pullToNote4 = [ MusicTheory.pitchToNotes[(note4Index+1)%12], MusicTheory.pitchToNotes[(note4Index+11)%12] ] 
            


            self.ChordProgressions[currChord] = collections.OrderedDict()

            self.ChordProgressions[currChord]['obvious'] = { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': {} }
            self.ChordProgressions[currChord]['unusual'] = { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': {} }
            self.ChordProgressions[currChord]['obscure'] = { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': {}, 'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': {} }

            currChordNotes = MusicTheory.AllChords[currChord]             

            for nextChord in MusicTheory.AllChords : 
                cnt += 1

                nextChordNotes = MusicTheory.AllChords[nextChord] 
        
                numCommonNotesBetweenChords = len ( list(set(currChordNotes).intersection(nextChordNotes)))  

                if ( currScale in MusicTheory.ChordsToScale[nextChord] ) : 
                    nextScale = currScale 
                else : 
                    nextScale = MusicTheory.ChordsToScale[nextChord][0]              

                notesInNextScale = MusicTheory.NotesInScale[nextScale]
            
                numNotCommonNotesBetweenScalePenalty = len(list(set(notesInCurrScale) - set(notesInNextScale))) * -1
                if (  numNotCommonNotesBetweenScalePenalty == 0 ) : 
                    numNotCommonNotesBetweenScalePenalty = 3    

                pullToHomeNoteIntersection = len ( list(set(pullToHome).intersection(nextChordNotes)))  * -4
                pullToNote1Intersection    = len ( list(set(pullToNote1).intersection(nextChordNotes))) * -3
                pullToNote2Intersection    = len ( list(set(pullToNote2).intersection(nextChordNotes))) * -2

                if ( SeventhChord ) : 
                    pullToNote3Intersection = len ( list(set(pullToNote3).intersection(nextChordNotes))) * -1
                else : 
                    pullToNote3Intersection = 0 

                if ( NinthChord ) : 
                    pullToNote4Intersection = len ( list(set(pullToNote4).intersection(nextChordNotes))) * -1
                else : 
                    pullToNote4Intersection = 0 


                pullNotesPenalty = pullToHomeNoteIntersection + pullToNote1Intersection + pullToNote2Intersection + pullToNote3Intersection + pullToNote4Intersection
                
                totalPenalty = pullNotesPenalty + numCommonNotesBetweenChords + numNotCommonNotesBetweenScalePenalty

                if ( nextChord.endswith ( 'Dim' )  ) : 
                    totalPenalty -= 15   # diminished chord penalty


                if ( totalPenalty < maxPenalty ) : 
                    maxPenalty = totalPenalty
                if ( totalPenalty > minPenalty ) : 
                    minPenalty = totalPenalty

                
                    

                #if ( currChord == 'CMajor' ) : 
                #    print ( "Next Chord: ", nextChord, "next scale: ", nextScale, "CurrChord: ", currChord, "curr scale: ", currScale ) 

                if ( 0 and (currChord == 'CMajor' or currChord == 'EMinor' ))  : 
                    print ( "CurrChord: " , currChord, "CurrScale: ", currScale, "NextChord: ", nextChord, "NextScale: ", nextScale, "Penalty: ", totalPenalty ) 
                #print ( totalPenalty ) 
                if ( totalPenalty  not in penaltyFreqDict ) : 
                    penaltyFreqDict[totalPenalty] = 1
                else : 
                    penaltyFreqDict[totalPenalty] += 1

                #Max Penalty seen = -24, Min Penalty seen: 4
                #Penalty range : 4 to -4 : obvious
                if ( totalPenalty >= -4 ) : 
                    # 4, 3, 2, 1: small
                    # 0, -1, -2: mid
                    # -3, -4: big
                    if ( totalPenalty >= 0 ) : 
                        self.ChordProgressions[currChord]['obvious']['PLAY_CHORD_PROGRESSION_TONE_SML_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                    elif ( totalPenalty >= -2 and totalPenalty <= 0 ) : 
                        self.ChordProgressions[currChord]['obvious']['PLAY_CHORD_PROGRESSION_TONE_MID_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                    elif ( totalPenalty >= -4 and totalPenalty <= -3 ) : 
                        self.ChordProgressions[currChord]['obvious']['PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                                            
                #Penalty range : -5 to -15 : unusual 
                elif ( totalPenalty >= -15 and totalPenalty <= -5 ) : 
                    # -5  to -8 : small
                    # -9  to -12: mid
                    # -13 to -15: big
                    if ( totalPenalty >= -8 and totalPenalty <= -5 ) : 
                        self.ChordProgressions[currChord]['unusual']['PLAY_CHORD_PROGRESSION_TONE_SML_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                    elif ( totalPenalty >= -12 and totalPenalty <= -9 ) : 
                        self.ChordProgressions[currChord]['unusual']['PLAY_CHORD_PROGRESSION_TONE_MID_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                    elif ( totalPenalty >= -15 and totalPenalty <= -13 ) : 
                        self.ChordProgressions[currChord]['unusual']['PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 


                #Penalty range : -16 to -24 : obscure
                elif ( totalPenalty >= -24 and totalPenalty <= -16 ) : 
                    # -16  to -18: small
                    # -19  to -21: mid
                    # -22  to -24: big
                    if ( totalPenalty >= -18 and totalPenalty <= -16 ) : 
                        self.ChordProgressions[currChord]['obscure']['PLAY_CHORD_PROGRESSION_TONE_SML_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                    elif ( totalPenalty >= -21 and totalPenalty <= -19 ) : 
                        self.ChordProgressions[currChord]['obscure']['PLAY_CHORD_PROGRESSION_TONE_MID_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                    elif ( totalPenalty >= -24 and totalPenalty <= -22 ) : 
                        self.ChordProgressions[currChord]['obscure']['PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP'][nextChord] = ( nextChord, nextScale, numCommonNotesBetweenChords, numNotCommonNotesBetweenScalePenalty, pullNotesPenalty, totalPenalty ) 
                    



        if ( 0 ) :
            if ( 0 ) :
                for i in range ( maxPenalty, minPenalty+1, 1 ) : 
                    print ( "Penalty: ", i, "Freq: ", penaltyFreqDict[i], "Pct: ", (penaltyFreqDict[i]*100)/cnt ) 
                    
            print ( "Max Penalty: ", maxPenalty ) 
            print ( "Min Penalty: ", minPenalty ) 

            #self.printChordProgressions ()

            #sys.exit(0) 
        

    def printChordProgressions ( self ) : 

        for chord in self.ChordProgressions :
            
            #if ( chord != 'CMajor' and chord != 'EMinor' ) : 
            if ( chord != 'CMajor' ) : 
                continue
            print ( "\tChord: ", chord ) 

            for movementType in self.ChordProgressions[chord] :
                
                print ( "\t\t", movementType ) 
                
                for progJump in self.ChordProgressions[chord][movementType] :
                    
                    print ( "\t\t\t", progJump ) 

                    for nextChord in self.ChordProgressions[chord][movementType][progJump] :


                            print ( "\t\t\t\t\t", self.ChordProgressions[chord][movementType][progJump][nextChord] ) 
