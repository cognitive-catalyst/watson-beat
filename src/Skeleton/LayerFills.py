from __future__ import print_function

import os
import sys
import random
import Section
import Constants
import collections
import MusicTheory
class LayerFills : 
    
    def __init__ ( self, phrase, tse, pl ) : 
        
        self.phrase = phrase 
        self.tse = tse
        self.pl = pl
        self.numSixteenthNotes = Constants.TSEs[self.tse]['num16thBeats'] 

    def getMeasureAndBeatDataForPhrase ( self ) : 

        if ( 1 ) : 
            print ( "tse: ", self.tse, "Phrase Length: ", self.pl ) 

        oneMeasureTicks   = Constants.TSEs[self.tse]['oneMeasure']

        self.measures = collections.OrderedDict()
        self.measures['main'] = collections.OrderedDict()

        self.excludedMeasures = {} 

        startTick = 0
        endTick = 0 

        for item in self.phrase :                
            for note in range(len(item['notes'])) : 
                duration = item['duration'][note] 
                endTick  = startTick + duration
                    
                mnum = ( startTick // oneMeasureTicks ) + 1
                beatNum = ( ( startTick // Constants.NoteDurationDict['sixteenth'] ) % self.numSixteenthNotes ) + 1

                if ( mnum not in self.measures['main'] ) : 
                    self.measures['main'][mnum] = collections.OrderedDict() 
                    currChord = item['chord']
                    currScale = item['scale'] 
                    
                # if the measure has two different scales or two different chords or both, it will not be a candidate for a fill
                if ( item['chord'] != currChord or item['scale'] != currScale ) :                        
                    self.excludedMeasures[mnum] = True
                    if ( 1 ) :
                        print ( "Measure Num : ", mnum , " will not have a fill " ) 

                if ( 1 ) :
                    print ( "Measure: ", mnum, "Beat: ", beatNum, "Note: ", item['notes'][note], 'scale:', item['scale'], 'chord:', item['chord'], 'duration:', duration, "startTick: ", startTick, "endTick: ", endTick  ) 

                velocity = item['velocity'][note]
                self.measures['main'][mnum][beatNum] = { 'note': item['notes'][note], 'scale': item['scale'], 'chord': item['chord'], 'duration': duration, 'velocity': velocity, 'startTick': startTick, 'endTick': endTick, 'pitch': item['pitches'][note] }  
                #self.measures['main'][mnum][beatNum] = { 'note': item['notes'][note], 'scale': item['scale'], 'chord': item['chord'], 'duration': duration, 'velocity': item['velocity'][note], 'startTick': startTick, 'endTick': endTick, 'pitch': item['pitches'][note] }  
                startTick = endTick                
        

        minBeatGranularity = 0.25 # this indicates we can start the fill after a quarter of the measure has passed
        maxBeatGranularity = 0.65 # this indicates no beats after 65% of the measure has passed will be used as a starting point of the fill 
        self.measures['alt1'] = self.getAlternativeMeasures( minBeatGranularity, maxBeatGranularity ) 
        #self.measures['alt2'] = self.getAlternativeMeasures( minBeatGranularity, maxBeatGranularity ) 

        if ( 1 ) : 
            for type in self.measures :
                print ( type , "Measures" ) 
                for mnum in self.measures[type] : 
                    for beatnum in self.measures[type][mnum] : 
                        print ( "Measure: ", mnum, "BeatNum: ", beatnum, self.measures[type][mnum][beatnum] ) 
                    print() 
                print() 


        return self.measures


    def getAlternativeMeasures ( self, minBeatGranularity, maxBeatGranularity ) : 

        quarterBeat = ( self.numSixteenthNotes / 4 ) + 1
        halfBeat    = ( self.numSixteenthNotes / 2 ) + 1
        fullBeat    = 1

        fillBeatsForMeasures = collections.OrderedDict() # record which are the fill beats we can start using for the fills
        alternativeMeasures  = collections.OrderedDict() 

        for mnum in self.measures['main'] : 
            if ( mnum in self.excludedMeasures ) : # this measure has either two scales or two chords or both. 
                # measure is not a candidate for fills, because it may have two different scales or chords or both
                alternativeMeasures[mnum] = self.measures['main'][mnum]
                print ( "Measure Num : ", mnum , " will not have a fill " ) 
                continue
         
            while ( quarterBeat > 1 ) : 
                if ( quarterBeat not in self.measures['main'][mnum] and quarterBeat > 1 ) : 
                    quarterBeat -= 1 
                if ( quarterBeat in self.measures['main'][mnum] and quarterBeat > 1 ) : 
                    mod = self.measures['main'][mnum][quarterBeat]['startTick'] % Constants.NoteDurationDict['sixteenth'] 
                    if ( mod == 0 ) : # if the note actually starts in a 16th note boundary break
                        break 
                    else : 
                        quarterBeat -= 1 
            if ( self.measures['main'][mnum][quarterBeat]['startTick'] % Constants.NoteDurationDict['sixteenth'] != 0 ) : 
                # measure is not a candidate for fills, because it may have two different scales or chords or both
                alternativeMeasures[mnum] = self.measures['main'][mnum]
                print ( "Measure Num : ", mnum , " will not have a fill " ) 
                continue
                
            while ( halfBeat > 1 ) : 
                if ( halfBeat not in self.measures['main'][mnum] and halfBeat > 1 ) : 
                    halfBeat -= 1 
                if ( halfBeat in self.measures['main'][mnum] and halfBeat > 1 ) : 
                    mod = self.measures['main'][mnum][halfBeat]['startTick'] % Constants.NoteDurationDict['sixteenth'] 
                    if ( mod == 0 ) : # if the note actually starts in a 16th note boundary break
                        break 
                    else : 
                        halfBeat -= 1 
            if ( self.measures['main'][mnum][halfBeat]['startTick'] % Constants.NoteDurationDict['sixteenth'] != 0 ) : 
                # measure is not a candidate for fills, because it may have two different scales or chords or both
                alternativeMeasures[mnum] = self.measures['main'][mnum]
                print ( "Measure Num : ", mnum , " will not have a fill " ) 
                continue
                

            #print ( "quarterBeat: ", quarterBeat, "halfBeat: ", halfBeat, "fullBeat: ", fullBeat )             
            #fillBeatsForMeasures[mnum] = []
            #for beatnum in self.measures['main'][mnum] :                 
            #    beatGranularity = float ( beatnum / (self.numSixteenthNotes*1.0) ) 
            #    if ( beatGranularity >= minBeatGranularity and beatGranularity <= maxBeatGranularity ) : 
            #        fillBeatsForMeasures[mnum].append ( beatnum ) 

            fillBeatForMeasure = random.choice ( [ quarterBeat, halfBeat, fullBeat ] ) 
            alternativeMeasures[mnum] = collections.OrderedDict() 

            prevPitch = self.measures['main'][mnum].values()[0]['pitch']
            homePitch = self.measures['main'][mnum].values()[0]['pitch']
            print ( "HomePitch: ", homePitch, "fillBeatForMeasure: ", fillBeatForMeasure ) 
            for beatnum in self.measures['main'][mnum] : 
                if ( beatnum == fillBeatForMeasure ) : 
                    if ( 1 ) : 
                        print ( "FILL BEAT Measure: ", mnum, "BeatNum: ", beatnum ) 
                    durationLeft = ( self.numSixteenthNotes - beatnum + 1 ) * Constants.NoteDurationDict['sixteenth']
                    alternativeMeasures[mnum].update ( self.getMiniMotive ( durationLeft, self.measures['main'][mnum][beatnum]['scale'], self.measures['main'][mnum][beatnum]['chord'], beatnum, self.measures['main'][mnum][beatnum]['startTick' ], prevPitch, homePitch ) )
                    break 
                else : 
                    alternativeMeasures[mnum][beatnum] = self.measures['main'][mnum][beatnum]
                prevPitch = self.measures['main'][mnum][beatnum]['pitch']
                    

        if ( 0 ) : 
            for mnum in alternativeMeasures : 
                for beatnum in alternativeMeasures[mnum] : 
                    print ( "Measure: ", mnum, "BeatNum: ", beatnum, alternativeMeasures[mnum][beatnum] ) 
                print() 

        return alternativeMeasures


    def getMiniMotive ( self, duration, scale, chord, beatnum, startTick, prevPitch, homePitch ) : 

        if ( duration <= Constants.NoteDurationDict['quarter'] ) : #480
            numNotesInMiniMotive = random.choice ( [1, 2, 2, 3] ) 
            NoteDurationList = [ Constants.NoteDurationDict['sixteenth'] ]
        elif ( duration <= Constants.NoteDurationDict['threeEights'] ) :  #720 
            numNotesInMiniMotive = random.choice ( [2, 3] ) 
            NoteDurationList = [ Constants.NoteDurationDict['sixteenth'], Constants.NoteDurationDict['eighth'] ]
        elif ( duration <= Constants.NoteDurationDict['half'] ) : #960
            numNotesInMiniMotive = random.choice ( [2, 3, 3] ) 
            NoteDurationList = [ Constants.NoteDurationDict['sixteenth'], Constants.NoteDurationDict['eighth'], Constants.NoteDurationDict['threeSixteenth'] ] 
        elif ( duration <= Constants.NoteDurationDict['threeQuarters'] ) : #1440
            numNotesInMiniMotive = random.choice ( [2, 3, 3, 4, 4] ) 
            NoteDurationList = [ Constants.NoteDurationDict['sixteenth'], Constants.NoteDurationDict['eighth'], Constants.NoteDurationDict['threeSixteenth'] ] 
        else :
            numNotesInMiniMotive = random.choice ( [2, 3, 3, 4, 5] ) 
            NoteDurationList = [ Constants.NoteDurationDict['sixteenth'], Constants.NoteDurationDict['eighth'], Constants.NoteDurationDict['threeSixteenth'], Constants.NoteDurationDict['quarter'] ] 




        while True : 

            numNotesInMiniMotive = random.choice ( [2, 3, 3, 3, 4, 4, 4, 5] ) 
            NoteDurationList     = [ Constants.NoteDurationDict['sixteenth'], Constants.NoteDurationDict['sixteenth'], Constants.NoteDurationDict['sixteenth'],  Constants.NoteDurationDict['eighth'], Constants.NoteDurationDict['threeSixteenth'], Constants.NoteDurationDict['sixteenth'], Constants.NoteDurationDict['eighth'], Constants.NoteDurationDict['threeSixteenth'], Constants.NoteDurationDict['quarter'] ] 
            durationPerMotive = duration // numNotesInMiniMotive
            mod = durationPerMotive % Constants.NoteDurationDict['sixteenth']
            if ( mod != 0 and mod >= 60 ) : 
                durationPerMotive += (Constants.NoteDurationDict['sixteenth']-mod) 
            else : 
                durationPerMotive -= mod 
        
            #print ( "Mini Motive Duration: ", duration, "Scale: ", scale, "chord: ", chord , "Duration Per Motive: ", durationPerMotive, "Num Notes In Motive: ", numNotesInMiniMotive ) 
        
            sum = 0 
            miniMotive = collections.OrderedDict () 
            for i in range ( numNotesInMiniMotive ) : 
                noteDuration = random.choice ( NoteDurationList ) 
                miniMotive[i] = { 'duration': noteDuration } 
                #print ( "Note: ", i+1, "Total Notes: ", numNotesInMiniMotive, "NoteDuration: ", noteDuration ) 
                sum += noteDuration
            if ( sum == durationPerMotive ) : 
                break 
            #print ( "Try Again: ", sum, durationPerMotive, duration ) 


        if ( 1 ) :
            print ( "Mini Motive Duration: ", duration, "Scale: ", scale, "chord: ", chord , "Duration Per Motive: ", durationPerMotive, "Num Notes In Motive: ", numNotesInMiniMotive ) 
        homeOctave = 5
        for item in miniMotive : 

            
            miniMotive[item]['note']  = random.choice ( MusicTheory.PentatonicScale[scale] + MusicTheory.NotesInScale[scale] ) 
            miniMotive[item]['pitch'] = self.getOctavesAndPitchData ( miniMotive[item]['note'], prevPitch, homePitch ) 
            prevPitch = miniMotive[item]['pitch']

            if ( 1 ) : 
                print ( item, miniMotive[item] )             

        currTicks  = 0 
        exitFlag   = False
        altMeasure = collections.OrderedDict()        
        while currTicks < duration : 

            for item in miniMotive : 
                if ( currTicks + miniMotive[item]['duration'] <= duration ) : 
                    altMeasure[beatnum] = { 'note': miniMotive[item]['note'], 'scale': scale, 'chord': chord, 'duration': miniMotive[item]['duration'], 'velocity': random.randint(50,80), 'startTick': startTick, 'endTick': startTick + miniMotive[item]['duration'], 'pitch': miniMotive[item]['pitch']  }                    
                    currTicks += miniMotive[item]['duration']
                    startTick += miniMotive[item]['duration']
                    beatnum = ( ( startTick // Constants.NoteDurationDict['sixteenth'] ) % self.numSixteenthNotes ) + 1
                else : 
                    exitFlag = True 
                    break
            if ( exitFlag ) : 
                break 
        
        if ( 1 ) : 
            print ( "Alternative Measure" ) 
            for beat in altMeasure : 
                print ( "Beat: ", beat, altMeasure[beat] ) 
            print() 
    
        return altMeasure

    def getOctavesAndPitchData ( self, note, prevPitch, homePitch ) : 

        octave = prevPitch // 12

        currNoteIndex = MusicTheory.NotesToPitch[note] 
        noteA = ( octave * 12 ) + currNoteIndex            
        if ( abs(noteA - homePitch) > 12 ) : 
            noteA = 1000

        if ( (octave + 1) >= 8 ) : 
            noteB = 1000 
        else : 
            noteB = ( (octave+1) * 12 ) + currNoteIndex
            if ( abs(noteB - homePitch) > 12 ) : 
                noteB = 1000

        if ( (octave - 1) < 4 ) : 
            noteC = 1000
        else : 
            noteC = ( (octave-1) * 12 ) + currNoteIndex 
            if ( abs(noteC - homePitch) > 12 ) : 
                noteC = 1000

        diffA = abs (prevPitch - noteA ) 
        diffB = abs (prevPitch - noteB )  
        diffC = abs (prevPitch - noteC )  
            
        print ( "diff: " , diffA, diffB, diffC ) 


        if ( diffA <= diffB and diffA <= diffC ) : 
            pitch = noteA
        elif ( diffB <= diffA and diffB <= diffC ) : 
            pitch = noteB 
        elif ( diffC <= diffA and diffC <= diffB ) : 
            pitch = noteC


        return pitch
