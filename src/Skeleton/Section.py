from __future__ import print_function

import os
import sys
import copy
import random
import collections

import Bass1
import Bass2
import Bass3
import Rhythm
import BrassRhythms

import Constants
import MidiOutput
import Pentatonic
import LayerFills
import MusicTheory
import AccompanyingLayers


from Percussions import Percussions

class Section: 
    
    def __init__ ( self, wbLevers, wbServerData ) :
        '''
        example wbLevers: 
            wbLevers = {
            'mood'        : mood,
            'complexity'  : complexityKnob, 
            'phraseLength': pl,
            'tse'         : tse, 
            'primaryScale': primaryScale, 
            'id'          : 0, 
            }
        '''

        self.wbLevers = wbLevers 
        self.layers = collections.OrderedDict()          
        
        # Intitialize the default bass layer 
        self.bass1Obj = Bass1.Bass1 ( self.wbLevers, wbServerData['bass1']['0'] ) 

        self.layers['bass1'] = self.bass1Obj.Chords

        self.bassRhythms = collections.OrderedDict() 

        # Initialize the bass1 rhythm for the section.
        self.rhy = Rhythm.Rhythm ( wbLevers )   # wbLevers['bassRhy'] gives the chord durations for the bass

        self.numChords = len(self.rhy.ChordDurations) 

        # needed for dj watson melody
        self.chordDict = collections.OrderedDict() 
        phraseNum = 0 
        for chordId in range(self.numChords) : 
            self.chordDict[chordId] = { 'duration': self.bass1Obj.Chords[phraseNum][chordId][0]['duration'][0], 'chord': self.bass1Obj.Chords[phraseNum][chordId][0]['chord'], 'scale':  self.bass1Obj.Chords[phraseNum][chordId][0]['scale'] } 

        # Initialize and run Melody 5 layer
        self.layers['mel5'] = self.initializeWatsonMelody ( wbServerData['mel5']['0'] ) 

    
    def PrintClassInfo ( self ) : 
        print() 
        print ( "WB Levers:" , self.wbLevers ) 
        self.bass1Obj.PrintClassInfo () 
        

    def run ( self ) :         

        if ( 0 ) : 
            for lyr in self.layers : 
                print ( "Layer: ", lyr ) 
                for num in range(len(self.layers[lyr] ) ) : 
                    for chordId in range(len(self.layers[lyr][num]) ) : 
                        print ( "Chord Id: ", chordId )
                        for item in range(len(self.layers[lyr][num][chordId]) ) : 
                            print ( num, item, self.layers[lyr][num][chordId][item] ) 
                        print() 

                print()
            print() 
        
        if ( 1 ) : 
            print ( "AT Client" ) 


        # Initialize and run Bass 2 layer
        self.layers['bass2'] = self.initializeAndRunBass2 () 

        if ( self.wbLevers['bassRhythmOptions'] != None ) : 
            # Initialize and run Bass 3 layer
            self.layers['bass3'], self.layers['brassRhythms']  = self.initializeAndRunBass3 () 
            

        layers = ['piano1', 'peruvianRhythmChords',  'rhythmChords', 'strings2' ]
        self.layers.update ( self.runAccompanyingLayers( layers ) ) 

        self.layers.update ( self.runPercussionLayers() ) 
        return self.layers


    def initializeWatsonMelody ( self, wbServerMelData ) :

        phraseNum = 0 
        self.mel5Data = collections.OrderedDict()  # collection of Phrases
        self.mel5Data[phraseNum] = collections.OrderedDict()  # collection of chords within phrase
        
        for chId in range(len(wbServerMelData)) : 
            self.mel5Data[phraseNum][chId] = wbServerMelData[str(chId)] 

        if ( 0 ) : 
            print() 
            print ( "-------------------------------- DJ MEL Starts --------------------------------------" ) 

        if ( 0 ) : 
            print ( "DJ Mel 5 Data, Phrase 1" ) 
            for chId in range(len(self.mel5Data[phraseNum] )) :
                print ( "\tChord Id: ", chId ) 
                for item in range(len(self.mel5Data[phraseNum][chId] )) :                 
                    print ( "\t\tNum: ", item, "Data: ", self.mel5Data[phraseNum][chId][item] )                  
                print() 


        if ( 0 ) : 
            print() 
            print ( "-------------------------------- DJ MEL Ends --------------------------------------" ) 


        return self.mel5Data


    def printLayers ( self ) : 

        print ( "Bass 1: " ) 
        self.bass1Obj.printTrainedData() 

    def initializeAndRunBass2 ( self ) :

        self.bass2Objs = [] 
        bass2TrainedData = [] 
        
        if ( 1 ) : 
            print ( "-------------------------------- BASS 2 Starts --------------------------------------" ) 
            print() 

        phraseNum = 0 
        # bass2Data structure: Dictionary of Dictionary of lists.
        # 1st dictionary is for phrase
        # 2nd dictinary is for chord in phrase
        # list is for item in phrase and chord
        self.bass2Data = collections.OrderedDict()  # collection of Phrases
        self.bass2Data[phraseNum] = collections.OrderedDict()  # collection of chords within phrase
        
        for chordId in range(len(self.rhy.ChordDurations)) : 
            
            chord = self.bass1Obj.Chords[phraseNum][chordId][0]['chord']
            scale = self.bass1Obj.Chords[phraseNum][chordId][0]['scale']
            duration = self.bass1Obj.Chords[phraseNum][chordId][0]['duration'][0]
            rhythm = self.rhy.chordTemplate[duration]['firstChoice']
            rhythm = [ Constants.NoteDurations[key]['ticks'] for key in rhythm ] 

            if ( 0 ) : 
                print ( "Initializing Chord: ", chordId, " Scale: ", scale, "Chord: ", chord , "Duration: ", duration, "Rhythm: ", rhythm  ) 
            
            bass2 = Bass2.Bass2 ( self.wbLevers,  scale, chord, duration, rhythm ) 
            bass2TrainedData = bass2.run() 
            
            self.bass2Data[phraseNum][chordId] = bass2TrainedData 

            if ( 0 ) : 
                for key in  bass2TrainedData : 
                    print ( key ) 

        if ( 0 ) : 
            print ( "Bass 2 Data, Phrase 1" ) 
            for chId in range(len(self.bass2Data[phraseNum] )) :
                print ( "\tChord Id: ", chId ) 
                for item in range(len(self.bass2Data[phraseNum][chId] )) :                 
                    print ( "\t\t Item Num: ", item, "Data: ", self.bass2Data[phraseNum][chId][item] )                  
                print() 

        if ( 1 ) : 
            print() 
            print ( "-------------------------------- BASS 2 Ends --------------------------------------" ) 

        return self.bass2Data 
        


    def initializeAndRunBass3 ( self ) :
        
        
        if ( 1 ) : 
            print ( "-------------------------------- BASS 3 Starts --------------------------------------" ) 
            print() 

        phraseNum = 0 
        # bass2Data structure: Dictionary of Dictionary of lists.
        # 1st dictionary is for phrase
        # 2nd dictinary is for chord in phrase
        # list is for item in phrase and chord
        self.bass3Data = collections.OrderedDict()  # collection of Phrases
        self.bass3Data[phraseNum] = collections.OrderedDict()  # collection of chords within phrase

        self.brassRhyData = collections.OrderedDict()  # collection of Phrases
        self.brassRhyData[phraseNum] = collections.OrderedDict()  # collection of chords within phrase


        numChords = len(self.rhy.ChordDurations)
        rhythmOptions =  self.wbLevers['bassRhythmOptions'] 
        numRhyOptions = len( rhythmOptions ) - 1
        rhyOption1 = random.randint ( 0, numRhyOptions ) 
        while ( True ) :
            rhyOption2 = random.randint ( 0, numRhyOptions ) 
            if ( rhyOption2 != rhyOption1 ) : 
                break 

        rhy1 = Bass3.getRhyDurations ( rhythmOptions[rhyOption1] , self.wbLevers['tse'] ) 
        rhy2 = Bass3.getRhyDurations ( rhythmOptions[rhyOption2] , self.wbLevers['tse'] ) 
        

        self.bassRhythms[0] = { i : {} for i in rhythmOptions[rhyOption1] }
        self.bassRhythms[1] = { i : {} for i in rhythmOptions[rhyOption2] }


        if ( 0 ) : 
            print ( "Bass Rhythm Option 1: " , rhythmOptions[rhyOption1], rhy1 ) 
            print ( "Bass Rhythm Option 2: " , rhythmOptions[rhyOption2], rhy2 ) 


        for chordId in range(numChords) :
            
            if ( chordId != numChords-1 ) : 
                bassRhy = rhy1
            else :
                bassRhy = rhy2

            chord = self.bass1Obj.Chords[phraseNum][chordId][0]['chord']
            scale = self.bass1Obj.Chords[phraseNum][chordId][0]['scale']
            duration = self.bass1Obj.Chords[phraseNum][chordId][0]['duration'][0]


            if ( 0 ) : 
                print() 
                print ( "Initializing Chord: ", chordId, " Scale: ", scale, "Chord: ", chord , "Duration: ", duration, "Rhythm Options: ", rhythmOptions, "chosen rhy option: ", bassRhy  ) 

            bass3 = Bass3.Bass3 ( self.wbLevers,  scale, chord, duration, bassRhy   ) 
            bass3TrainedData = bass3.run()             

            self.bass3Data[phraseNum][chordId] = bass3TrainedData 

            brassRhy = BrassRhythms.BrassRhythm ( self.wbLevers,  scale, chord, duration, bassRhy )
            brassRhyTrainedData = brassRhy.run()             
            self.brassRhyData[phraseNum][chordId] = brassRhyTrainedData 

            if ( 0 ) : 
                for key in  bass3TrainedData : 
                    print ( key ) 

        if ( 0 ) : 
            print ( "Bass 3 Data, Phrase 1" ) 
            for chId in range(len(self.bass3Data[phraseNum] )) :
                print ( "\tChord Id: ", chId ) 
                for item in range(len(self.bass3Data[phraseNum][chId] )) :                 
                    print ( "\t\t Item Num: ", item, "Data: ", self.bass3Data[phraseNum][chId][item] )                  
                print() 

        if ( 1 ) : 
            print() 
            print ( "-------------------------------- BASS 3 Ends --------------------------------------" ) 


        return self.bass3Data, self.brassRhyData



    def runAccompanyingLayers ( self, layers ) :
        
        accompanyingLayers   = AccompanyingLayers.AccompanyingLayers ( layers, self.bass1Obj, self.rhy.UniqueChordDurations, self.chordDict, self.wbLevers ) 
        accLayersTrainedData = accompanyingLayers.initializeAndRunLayers ()         
        return accLayersTrainedData
    

    def runPercussionLayers ( self ) : 
        
        percussionLayers = Percussions.Percussions ( self.wbLevers, self.bassRhythms ) 
        return ( percussionLayers.run() ) 
