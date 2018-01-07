from __future__ import print_function
from itertools import chain

import sys
import random
import collections

import DrumKit
import DrumFills
import KickDrums
import BassDrums
import SnareDrums
import HihatDrums
import CymbalSwell
import DrumConstants
import MarineraDrumKit
import LatinPopDrums
from Skeleton import Constants
from Skeleton import MusicTheory

class Percussions () : 
    '''
    '''

    def __init__ ( self, wbLevers, rhyOptions ) : 
        

        self.type = wbLevers['percussionSettings']['type']


        if ( self.type == 'defaultDrumKitSeparate' ) : 
            self.layerDescs = [ 'drumsKick', 'drumsSnare', 'drumsHihat', 'drumsCymbalSwell', 'drumsBass' ] 
        elif ( self.type == 'defaultDrumKit' ) : 
            self.layerDescs = [ 'drumsKit', 'drumsKick', 'drumsSnare', 'drumsHihat', 'drumsCymbalSwell', 'drumsBass' ] 
        elif ( self.type == 'peruvianMarinera' ) : 
            self.layerDescs = [ 'drumsKitMarinera' ]
        else : 
            self.layerDescs = [ 'drumsKick', 'drumsSnare', 'drumsHihat', 'drumsCymbalSwell', 'drumsBass', 'drumsKit' ] 

        if ( wbLevers['bassRhythmOptions'] != None ) : 
            self.layerDescs.append ( 'drumsLatinPop' )
            self.rhyOptions = rhyOptions
            #print ( rhyOptions ) 


        #self.layerDescs = [ 'drumsKick', 'drumsSnare', 'drumsHihat', 'drumsCymbalSwell', 'drumsBass', 'drumsKit' ] 
        self.percussionLayers = {}

        self.wbLevers = wbLevers 
        self.numEOSFills = 2   # num end of section fills
        self.numEOPFills = 2   # num end of phrase fills 
        self.BeatInfo = self.wbLevers['percussionSettings']['BeatInfo'] 
        self.Patterns = self.wbLevers['percussionSettings']['Patterns'] 
        self.numPatterns = len(self.Patterns) 



    def run ( self ) : 
        numBeats = Constants.TSEs[self.wbLevers['tse']]['num16thBeats'] 
        fills = True

        for lyr in self.layerDescs :             
            if lyr == 'drumsKick' : 
                self.percussionLayers['drumsKick'] = KickDrums.run( self.BeatInfo,   self.Patterns,  self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'])
            elif lyr == 'drumsBass' : 
                self.percussionLayers['drumsBass'] = BassDrums.run( self.BeatInfo,   self.Patterns,  self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'])
            elif lyr == 'drumsSnare' : 
                self.percussionLayers['drumsSnare'] = SnareDrums.run( self.BeatInfo, self.Patterns,  self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'])
            elif lyr == 'drumsHihat' : 
                self.percussionLayers['drumsHihat'] = HihatDrums.run( self.BeatInfo, self.Patterns,  self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'])
            elif lyr == 'drumsCymbalSwell' : 
                self.percussionLayers['drumsCymbalSwell'] = CymbalSwell.run( self.BeatInfo, self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'])
            elif lyr == 'drumsKit' : 
                self.percussionLayers['drumsKit'] = DrumKit.run( self.BeatInfo,   self.Patterns,  self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'])

            elif lyr == 'drumsKitMarinera' : 
                self.percussionLayers['drumsKitMarinera'] = MarineraDrumKit.run( self.BeatInfo,  self.Patterns,  self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'])
                fills = False

            elif lyr == 'drumsLatinPop' : 
                self.percussionLayers['drumsLatinPop'] = LatinPopDrums.run ( self.BeatInfo, self.Patterns, self.wbLevers['tse'], self.wbLevers['rhythmSpeed'], self.wbLevers['phraseLength'], self.rhyOptions)



        if ( fills ) : 

            emptyMeasure = collections.OrderedDict()

            emptyMeasure[1] = { 'beatNum': 1, 'event': 'on',  'note': 'C', 'velocity': 1, 'midiClk': 0, 'octave': 0, 'pitch': "midi.C_0" }
            emptyMeasure[2] = { 'beatNum': 1, 'event': 'off', 'note': 'C', 'velocity': 0, 'midiClk': 1, 'octave': 0, 'pitch': "midi.C_0" }
                      
            emptyMeasure[3] = { 'beatNum': 1, 'event': 'on',  'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } 
            emptyMeasure[4] = { 'beatNum': 1, 'event': 'off', 'note': DrumConstants.fillNotes['low']['kick'], 'velocity': 0, 'midiClk': numBeats*DrumConstants.SmallestGranularityInTicks-1, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } 
                      
           
            self.percussionLayers['fillsForDrums'] = collections.OrderedDict() 
                      
           
            self.percussionLayers['fillsForDrums']['eosFillsForDrums'] = collections.OrderedDict() 
            self.percussionLayers['fillsForDrums']['eopFillsForDrums'] = collections.OrderedDict() 
           
            for i in range(self.numPatterns) : 
                self.percussionLayers['fillsForDrums']['eosFillsForDrums'][i] = collections.OrderedDict() 
                eosStartBeat = self.Patterns[i]['eosStartBeat'] 
                totalBeats = numBeats + 1 - eosStartBeat
                df = DrumFills.DrumFill ( self.wbLevers['tse'], eosStartBeat, totalBeats, self.wbLevers['rhythmSpeed'], self.wbLevers['complexity'] ) 
                self.percussionLayers['fillsForDrums']['eosFillsForDrums'][i]['fillMeasure'] =  df.createFills() 
                self.percussionLayers['fillsForDrums']['eosFillsForDrums'][i]['emptyMeasure'] = emptyMeasure
           
                self.percussionLayers['fillsForDrums']['eopFillsForDrums'][i] = collections.OrderedDict() 
                eopStartBeat = self.Patterns[i]['eopStartBeat'] 
                totalBeats = numBeats + 1 - eopStartBeat
                df = DrumFills.DrumFill ( self.wbLevers['tse'], eopStartBeat, totalBeats, self.wbLevers['rhythmSpeed'], self.wbLevers['complexity'] ) 
                self.percussionLayers['fillsForDrums']['eopFillsForDrums'][i]['fillMeasure'] =  df.createFills() 
                self.percussionLayers['fillsForDrums']['eopFillsForDrums'][i]['emptyMeasure'] = emptyMeasure




        return self.percussionLayers 
