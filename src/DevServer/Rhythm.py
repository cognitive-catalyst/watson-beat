from __future__ import print_function

import sys
import random
import collections

import Constants

class Rhythm :
    

    def __init__ ( self, levers ) :

        self.ChordDurations = levers['bassRhy']
        self.numChordsInPL  = len(self.ChordDurations) 


        self.UniqueChordDurations = collections.OrderedDict() 
        uniqueChordDurations = list(set(self.ChordDurations)) 
        for duration in uniqueChordDurations : 
            self.UniqueChordDurations[duration] = []
            for chordId in range(len(self.ChordDurations)) : 
                if self.ChordDurations[chordId] == duration : 
                    self.UniqueChordDurations[duration].append( chordId )
                    
        
        self.levers = levers

        self.pl   = levers['phraseLength']        
        self.tse  = levers['tse']
        self.maxduration    = Constants.TSEs[self.tse]['oneMeasure'] * self.pl 
            
        self.fiveMeasureTicks    =  Constants.TSEs[self.tse]['oneMeasure'] * 5
        self.fourMeasureTicks    =  Constants.TSEs[self.tse]['oneMeasure'] * 4 
        self.threeMeasureTicks   =  Constants.TSEs[self.tse]['oneMeasure'] * 3 
        self.twoMeasureTicks     =  Constants.TSEs[self.tse]['oneMeasure'] * 2 
        self.fullMeasureTicks    =  Constants.TSEs[self.tse]['oneMeasure'] 
        self.halfMeasureTicks    =  Constants.TSEs[self.tse]['oneMeasure'] / 2 
        self.oneHalfMeasureTicks =  self.halfMeasureTicks * 3
        self.quarterMeasureTicks =  Constants.TSEs[self.tse]['oneMeasure'] / 4  


        self.chordTemplate   = self.createRhythmTemplates () 

        self.printRhythm() 

    def PrintClassInfo ( self ) : 
        
        print ( "Initializing Basic Rhythm for Chords" ) 
        print ( "Num Chords: ", self.numChordsInPL ) 
        print ( "Chord Durations: ", self.ChordDurations ) 
        print ( "Chord Durationtemplates: ", self.chordTemplate ) 
        print ()

                
    def setChordDurationTemplates ( self, ticksForChord ) : 
        '''
        Determines the rhythm inside the chord. 
        Let's say the chord is for half measure and the tse of 3/4. Then the duration of the chord is 720 ticks. ( 1/4 note = 480 ticks. measure = 480*3. half measure = ( 480 * 3 ) / 2 ) 
        This function determines the rhythm for this half meansure chord.
        Some possible breakdowns of 720 ticks
        120 120 480
        240, 480
        240, 240, 240
        etc.
        '''
        tryNum = 1
        while True : 
            currTicks = 0 
            chordSeq  = [] 
            while currTicks < ticksForChord :

                currNote = random.choice ( Constants.NoteDurations.keys() )           
                ticks = Constants.NoteDurations[currNote]['ticks']                
                if ( ticksForChord > 360 ) : 
                    #print ( currNote, ticks ) 
                    if ( self.levers['complexity'] == 'super_simple' ) : # avoid 16th notes for super simple
                        if ( ticks == 120 ) : 
                            continue
                    elif ( self.levers['complexity'] == 'simple' ) : # if complexity == simple, avoid having only a single 16th note. Always have them in pairs
                        if ( ticks == 120 ) : 
                            currTicks += Constants.NoteDurations[currNote]['ticks']
                            chordSeq.append ( currNote ) 

                currTicks += Constants.NoteDurations[currNote]['ticks']
                chordSeq.append ( currNote ) 
                #print ( ticksForChord, currTicks, chordSeq ) 

            if ( currTicks == ticksForChord ) : 
                break
            if ( 0 ) : 
                print ( "Try Number: ", tryNum, " Sequence not found: ", chordSeq )             
            tryNum += 1

        if ( 0 ) : 
            print ( "Sequence found in try number: ", tryNum, " Sequence : ", chordSeq ) 
        return ( chordSeq ) 



    def createRhythmTemplates ( self ) : 

        
        template = collections.OrderedDict()

        self.halfMeasureChordTemplate    = self.setChordDurationTemplates ( self.halfMeasureTicks )            
        self.fullMeasureChordTemplate    = self.setChordDurationTemplates ( self.fullMeasureTicks )
        self.oneHalfMeasureChordTemplate = self.setChordDurationTemplates ( self.oneHalfMeasureTicks )
        self.twoMeasureChordTemplate     = self.setChordDurationTemplates ( self.twoMeasureTicks )
        self.quarterMeasureChordTemplate = self.setChordDurationTemplates ( self.quarterMeasureTicks )
        

        template[self.quarterMeasureTicks] = collections.OrderedDict() 
        template[self.quarterMeasureTicks]['info']        = 'Quarter Measure Chord' 
        template[self.quarterMeasureTicks]['choices']     = [ self.quarterMeasureChordTemplate ] 
        template[self.quarterMeasureTicks]['firstChoice'] =  self.quarterMeasureChordTemplate 
        

        template[self.halfMeasureTicks] = collections.OrderedDict() 
        template[self.halfMeasureTicks]['info']        = 'Half Measure Chord' 
        template[self.halfMeasureTicks]['choices']     = [ self.halfMeasureChordTemplate ] 
        template[self.halfMeasureTicks]['firstChoice'] =  self.halfMeasureChordTemplate 
        


        template[self.fullMeasureTicks] = collections.OrderedDict()  
        template[self.fullMeasureTicks]['info']        = 'Full Measure Chord' 
        template[self.fullMeasureTicks]['choices']    = [ self.halfMeasureChordTemplate + self.halfMeasureChordTemplate, 
                                                                    self.fullMeasureChordTemplate, 
                                                                    self.fullMeasureChordTemplate] 
        template[self.fullMeasureTicks]['firstChoice'] = random.choice ( template[self.fullMeasureTicks]['choices'] ) 



        template[self.oneHalfMeasureTicks] = collections.OrderedDict()
        template[self.oneHalfMeasureTicks]['info']    = 'One Half Measure Chord' 
        template[self.oneHalfMeasureTicks]['choices'] = [ self.halfMeasureChordTemplate + self.halfMeasureChordTemplate + self.halfMeasureChordTemplate, 
                                                                    template[self.fullMeasureTicks]['firstChoice'] + self.halfMeasureChordTemplate, 
                                                                    self.halfMeasureChordTemplate + template[self.fullMeasureTicks]['firstChoice'], 
                                                                    self.oneHalfMeasureChordTemplate ] 
        template[self.oneHalfMeasureTicks]['firstChoice'] = random.choice ( template[self.oneHalfMeasureTicks]['choices'] ) 
        


        template[self.twoMeasureTicks] = collections.OrderedDict()  
        template[self.twoMeasureTicks]['info']        = 'Two Measure Chord' 
        template[self.twoMeasureTicks]['choices']     = [ self.halfMeasureChordTemplate + self.halfMeasureChordTemplate + self.halfMeasureChordTemplate + self.halfMeasureChordTemplate, 
                                                                    self.halfMeasureChordTemplate + template[self.oneHalfMeasureTicks]['firstChoice'],
                                                                    template[self.fullMeasureTicks]['firstChoice'] + template[self.fullMeasureTicks]['firstChoice'], 
                                                                    template[self.oneHalfMeasureTicks]['firstChoice'] + self.halfMeasureChordTemplate, 
                                                                    self.twoMeasureChordTemplate ] 
        template[self.twoMeasureTicks]['firstChoice'] = random.choice ( template[self.twoMeasureTicks]['choices'] ) 


        template[self.threeMeasureTicks] = collections.OrderedDict()  
        template[self.threeMeasureTicks]['info']        = 'Three Measure Chord' 
        template[self.threeMeasureTicks]['choices']     = [ template[self.fullMeasureTicks]['firstChoice'] + template[self.fullMeasureTicks]['firstChoice'] + template[self.fullMeasureTicks]['firstChoice'],  
                                                                      template[self.oneHalfMeasureTicks]['firstChoice'] + template[self.oneHalfMeasureTicks]['firstChoice'] ]            
        template[self.threeMeasureTicks]['firstChoice'] = random.choice ( template[self.threeMeasureTicks]['choices'] ) 
        
        
        template[self.fourMeasureTicks] = collections.OrderedDict()  
        template[self.fourMeasureTicks]['info']        = 'Four Measure Chord' 
        template[self.fourMeasureTicks]['choices']     = [ template[self.fullMeasureTicks]['firstChoice'] + template[self.fullMeasureTicks]['firstChoice'] + template[self.fullMeasureTicks]['firstChoice'] + template[self.fullMeasureTicks]['firstChoice'],
                                                                     template[self.oneHalfMeasureTicks]['firstChoice'] + template[self.oneHalfMeasureTicks]['firstChoice'] + template[self.fullMeasureTicks]['firstChoice'],
                                                                     template[self.twoMeasureTicks]['firstChoice'] + template[self.twoMeasureTicks]['firstChoice'] ] 
        template[self.fourMeasureTicks]['firstChoice'] = random.choice ( template[self.fourMeasureTicks]['choices'] ) 

        template[self.fiveMeasureTicks] = collections.OrderedDict()  
        template[self.fiveMeasureTicks]['info']        = 'Five Measure Chord' 
        template[self.fiveMeasureTicks]['choices']     = [ template[self.twoMeasureTicks]['firstChoice'] + template[self.threeMeasureTicks]['firstChoice'],
                                                                     template[self.threeMeasureTicks]['firstChoice'] + template[self.twoMeasureTicks]['firstChoice']  ] 
        template[self.fiveMeasureTicks]['firstChoice'] = random.choice ( template[self.fiveMeasureTicks]['choices'] ) 


        if ( 0 ) : 
            print() 
            print ( "Chord Durations: ", self.ChordDurations ) 
            for chord in self.ChordDurations : 
                print ( template[chord]['info'], template[chord]['firstChoice'] ) 

        return ( template ) 
            

    def printRhythm ( self ) : 

        if ( 0 ) : 
            print()
            print ( "Half Measure Chord Template: ", self.halfMeasureChordTemplate ) 
            print ( "Full Measure Chord Template: ", self.fullMeasureChordTemplate ) 
            print ( "One Half Measure Chord Template: ", self.oneHalfMeasureChordTemplate ) 
            print ( "Two Measure Chord Template: ", self.twoMeasureChordTemplate ) 


        if ( 0 ) : 
            for key in self.chordTemplate :
                print ( key, self.chordTemplate[key]['choices'],  self.chordTemplate[key]['firstChoice'] ) 
                print ( self.chordTemplate[key]['info'], ". Duration in ticks: ", key, "first choice: ", self.chordTemplate[key]['firstChoice'], "first choice ticks: ", self.chordTemplate[key]['firstChoice'] ) 
                for ch in self.chordTemplate[key]['choices'] : 
                    print ( "Choice Options; ", ch )
                print() 

        if ( 1 ) :
            #print ( "Chord Durations: ", self.ChordDurations ) 

            string = ""
            for chord in self.ChordDurations : 
                #print ( "Chord: ", chord, self.chordTemplate ) 
                string += str(chord) + " " + str(self.chordTemplate[chord]['firstChoice']) + " " 
                # print ( chord, self.chordTemplate[chord]['firstChoice'] ) 
            #print ( "Chord Rhythms", string ) 

            print() 


