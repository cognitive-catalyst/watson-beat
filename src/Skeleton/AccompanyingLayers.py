from __future__ import print_function
from itertools import chain

import os
import sys
import random
import Piano1
import Strings1
import Strings2
import Constants
import Pentatonic
import collections
import RhythmChords
import PeruvianRhythmChords 

class AccompanyingLayers : 

    def __init__ ( self, layers, bass1Chords, uniqueChords, chordDict, wbLevers ) : 
        
        self.layers   = layers
        self.speed    = wbLevers['rhythmSpeed']
        self.wbLevers = wbLevers
        self.numChords = len(bass1Chords.Chords[0])   # 0 indicates the phrase num 
        self.chordDict = chordDict 


        self.ids      = collections.OrderedDict() 
        self.chord    = collections.OrderedDict() 
        self.scale    = collections.OrderedDict() 
        self.duration = collections.OrderedDict() 


        for uniqChordDuration in uniqueChords : 

            self.ids[uniqChordDuration]   = [] 
            self.chord[uniqChordDuration] = [] 
            self.scale[uniqChordDuration] = []
            self.duration[uniqChordDuration] = 0

            for chId in uniqueChords[uniqChordDuration] : 

                # bass1Chords.Chords[0] => 0 indicates phrase 1
                # # bass1Chords.Chords[0][chId] => is a dictionary of dictionary of list
                # bass1Chords.Chords[0][chId][0] => chId indicates chord Id, last [0] indicates item number for that chord(which stores a list) 

                self.ids[uniqChordDuration].append ( chId ) 
                self.chord[uniqChordDuration].append ( bass1Chords.Chords[0][chId][0]['chord'])
                self.scale[uniqChordDuration].append ( bass1Chords.Chords[0][chId][0]['scale'] )
                self.duration[uniqChordDuration] = bass1Chords.Chords[0][chId][0]['duration'][0]



    def getChordSplitDuration ( self ) : 

        tse   = self.wbLevers['tse']
        speed = self.wbLevers['rhythmSpeed']
        durationOneMeasure  = Constants.TSEs[tse]['oneMeasure']
        durationHalfMeasure = Constants.TSEs[tse]['oneMeasure']/2

        if ( durationHalfMeasure in self.chord ) : 
            durationBreakdown = durationHalfMeasure
            halfMeasure = True
        else : 
            durationBreakdown = durationOneMeasure
            halfMeasure = False
        self.chordSplitDuration = {}

        self.chordSplitDuration[durationOneMeasure*0.5] = []
        self.chordSplitDuration[durationOneMeasure]     = []
        self.chordSplitDuration[durationOneMeasure*1.5] = []
        self.chordSplitDuration[durationOneMeasure*2]   = []
        self.chordSplitDuration[durationOneMeasure*3]   = []
        self.chordSplitDuration[durationOneMeasure*4]   = []
        

        if ( not self.wbLevers['complexity'].endswith('simple') ) : 
            return 
        

        if ( durationBreakdown in Constants.OtherChordDurationBreakdown ) : 

            chordSplitDuration = []
            split = random.choice ( Constants.OtherChordDurationBreakdown[durationBreakdown][speed] )
            for item in split : 
                chordSplitDuration.append ( random.choice ( Constants.MinChordDurationBreakdown[item][speed] ) )                 
            chordSplitDuration = list(chain.from_iterable(chordSplitDuration) )  # flatten array of arrays
                                          
        elif ( durationBreakdown in Constants.MinChordDurationBreakdown ) : 
            chordSplitDuration = random.choice ( Constants.MinChordDurationBreakdown[durationBreakdown][speed] )

        else : 
            print ( "Duration not initialized for Chord Split: ", durationBreakdown, "\nAbort\n" ) ;
            # DurationSplit = ChordDurationForLayers.createChordDurations ( durationBreakdown ) 
            sys.exit(0) 

            
        if ( halfMeasure )  : 
            self.chordSplitDuration[durationBreakdown]    = chordSplitDuration
            self.chordSplitDuration[durationOneMeasure]   = chordSplitDuration + chordSplitDuration
            chordSplitDuration = self.chordSplitDuration[durationOneMeasure]
        else : 
            self.chordSplitDuration[durationBreakdown]    = chordSplitDuration
        
        self.chordSplitDuration[durationOneMeasure*2] = chordSplitDuration + chordSplitDuration
        self.chordSplitDuration[durationOneMeasure*3] = chordSplitDuration + chordSplitDuration + chordSplitDuration
        self.chordSplitDuration[durationOneMeasure*4] = chordSplitDuration + chordSplitDuration + chordSplitDuration + chordSplitDuration 
        
        if ( 0 ) : 
            print ( halfMeasure ) 
            print ( "chordSplitDuration: ", chordSplitDuration ) 
            print ( "One Measure: ", durationOneMeasure, self.chordSplitDuration[durationOneMeasure] ) 
            print ( "two Measure: ", durationOneMeasure*2, self.chordSplitDuration[durationOneMeasure*2] ) 

    def initializeAndRunLayers ( self ) :

        TrainedData       = collections.OrderedDict()
        chordDataForLayer = collections.OrderedDict()

        for layer in self.layers : 
            chordDataForLayer[layer] = collections.OrderedDict()

            if ( layer == 'strings2' ) : 
                strings2 = Strings2.Strings2 ( self.wbLevers,  self.chordDict ) 
                chordDataForLayer[layer] = strings2.run() 
                for strClass in  chordDataForLayer[layer] : 
                    for instId in chordDataForLayer[layer][strClass] :
                        if ( chordDataForLayer[layer][strClass][instId][0]['desc']  == strClass ) :
                            desc = strClass # for arpstrings, leftPianoBass and rightPiano
                        else :  
                            desc = strClass + "_" + chordDataForLayer[layer][strClass][instId][0]['desc']  # for lostrings, midstrings and histrings
                        TrainedData[desc] = chordDataForLayer[layer][strClass][instId] 
                        if ( 0 ) : 
                            print ( desc, strClass )                        
                            for item in chordDataForLayer[layer][strClass][instId] : 
                                print ( item ) 


                # strings2  => TrainedData['lostrings, midstrings, histrings, arpstrings etc][phrase] at Section.py
                        
            else : 

                if ( layer == 'piano1' or layer == 'peruvianRhythmChords' ) : 

                    # for piano1: simple  : will not have 16th notes, and range is smaller
                    # for piano1: complex : will have 16th notes, range is larger , may have 7th and 9th chords too
                    # for peruvianRhythmChords:   simple  will only have quarter notes
                    # for peruvianRhythmChords:   complex will have some rhythm within the quarter notes from simple 
                    self.getChordSplitDuration ()                      
                    chordDataForLayer[layer]['simple']  = collections.OrderedDict()  
                    chordDataForLayer[layer]['complex'] = collections.OrderedDict()                      

                for key in self.chord :  # key holds the unique chord durations eg. [1920, 3840] etc

                    if ( layer == 'melP' ) : 
                        pMel = Pentatonic.PMelody ( self.wbLevers,  self.scale[key], self.chord[key], self.ids[key], self.duration[key] ) 
                        chordDataForLayer[layer].update (  pMel.run() )

                    elif ( layer == 'piano1' or layer == 'peruvianRhythmChords' ) : 
                        if ( 0 ) : 
                            print ( "Layer : ", layer, self.chordSplitDuration[self.duration[key]], self.duration[key] )

                        if ( layer == 'piano1' ) : 
                            piano1 = Piano1.Piano1 ( self.wbLevers,  self.scale[key], self.chord[key], self.ids[key], self.duration[key] )                         
                            simple, complex = piano1.run( self.chordSplitDuration[self.duration[key]] )
                        elif (  layer == 'peruvianRhythmChords' ) : 
                            peruvianRhythmChords = PeruvianRhythmChords.PeruvianRhythmChords ( self.wbLevers,  self.scale[key], self.chord[key], self.ids[key], self.duration[key] )
                            simple, complex = peruvianRhythmChords.run( ) 
                            
                        chordDataForLayer[layer]['simple'].update  ( simple )   
                        chordDataForLayer[layer]['complex'].update ( complex )   

                        if ( 0 ) : 
                            for chId in chordDataForLayer[layer]['simple'] :
                                print ( "ChordId: ", chId ) 
                                for item in chordDataForLayer[layer]['simple'][chId] :
                                    print ( "Item: ", item ) 

                    elif ( layer == 'rhythmChords' ) : 
                        rhyChords = RhythmChords.RhythmChords ( self.wbLevers,  self.scale[key], self.chord[key], self.ids[key], self.duration[key] ) 
                        chordDataForLayer[layer].update (  rhyChords.run() ) 

                    elif ( layer == 'strings1' ) : 
                        strings1 = Strings1.Strings1 ( self.wbLevers,  self.scale[key], self.chord[key], self.ids[key], self.duration[key] ) 
                        chordDataForLayer[layer].update (  strings1.run() ) 

                if ( layer == 'piano1'  or layer == 'peruvianRhythmChords' ) : 

                    TrainedData[layer] = collections.OrderedDict()  #TrainedData['piano'] = collections.ordereddict[chordIds]  => TrainedData['piano'][0], TrainedData['piano'][1] etc
                    for chordId in range(self.numChords) : 
                        TrainedData[layer][chordId] = collections.OrderedDict()  #TrainedData['piano'][0,1,2] = collections.ordereddict [simple, complex] => TrainedData['piano'][0]['simple'] , TrainedData['piano'][0]['complex'] 
                        for type in chordDataForLayer[layer] :  # type = simple or complex
                            TrainedData[layer][chordId][type] = [] 
                            for item in chordDataForLayer[layer][type][chordId] : 
                                TrainedData[layer][chordId][type] += item 

                else : 
                    TrainedData[layer] = collections.OrderedDict()  #TrainedData['rhythmChords'] = collections.ordereddict[chordIds]  => TrainedData['rhythmChords'][0], TrainedData['rhythmChords'][1] etc
                    for chordId in range(self.numChords) :
                        TrainedData[layer][chordId] = [] 
                        for item in  chordDataForLayer[layer][chordId] : 
                            TrainedData[layer][chordId] += item 

        if ( 0 ) :
            for layer in TrainedData :
                if ( layer == '1piano1' or layer == 'peruvianRhythmChords' or layer == '1rhythmChords' )  :  
                    print ( "Layer: " , layer ) 
                    for chordId in TrainedData[layer] : 
                        print ( "\tChord Id: ", chordId ) 
                        if ( layer == 'piano1' or layer == 'peruvianRhythmChords' )  : 
                            for type in TrainedData[layer][chordId] :  # type = simple, complex
                                print ( "\t\tType: ", type ) 
                                for item in TrainedData[layer][chordId][type] : 
                                    print ( "\t\t\titem: ", item ) 
                        elif ( layer == 'rhythmChords' )  : 
                            for item in TrainedData[layer][chordId] : 
                                print ( "\t\titem: ", item )                         
                    print() 
                elif ( layer.startswith('leftPianoBass') or layer.startswith('1arpStrings') ) :
                    print ( "Layer: " , layer ) 
                    for item in TrainedData[layer] :
                        print ( "\titem: ", item ) 
                    
        
        #sys.exit(0) 
        # piano1 => TrainedData['piano1'][chordId][type], at Section.py:  # type = 'simple' or 'complex'
        # rhythmChords => TrainedData['rhythmChords'][chordId], at Section.py: 
        # strings2  => TrainedData['lostrings, midstrings, histrings, arpstrings etc][phrase] at Section.py
        # peruvianRhythmChords => TrainedData['peruvianRhythmChords'][chordId][type], at Section.py:   # type = 'simple' or 'complex'

        return TrainedData


