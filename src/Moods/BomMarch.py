from __future__ import print_function
from Skeleton import MusicTheory
from Skeleton import Constants
from Skeleton import BassRhythms
from Arranging.Arranging import *
import InitializeSectionsHelper
import InitializeChordsAndPhraseHelper


import sys
import math
import random
import collections
class BomMarch: 

    def __init__ ( self, movement, selectedTempo ) : 
        
        self.complexity = movement['complexity'] 
        self.durationInSecs = movement['duration'] 
        self.rhythmSpeed = movement['rhythmSpeed'] 
        self.selectedTempo = selectedTempo 
        if ( 0 ) : 
            print ( "Mood: Bom March" ) 
            print ( 'Complexity: ', self.complexity ) 


        self.percussionDesc = ['drumsKick', 'drumsBass', 'drumsSnare' ] 

        self.layers = {
            'bass2': { 'density': 1, 'range': 'low', 'type': '' },
            'drumsKick': { 'density': 1, 'range': 'low', 'type': 'percussion'}, 
            'drumsBass': { 'density': 1, 'range': 'low', 'type': 'percussion'}, 


            'mel5' :   { 'density': 1, 'range': 'all', 'type': '' },
            'drumsSnare': { 'density': 1, 'range': 'mid', 'type': 'percussion'}, 
            'rightPiano': { 'density': 1, 'range': 'mid', 'type': '' },
            'rightPiano2': { 'density': 1, 'range': 'mid', 'type': '' },
            }
        
        
        self.notLoLayers = {

            'mel5' :   { 'density': 1, 'range': 'all', 'type': '' },
            'drumsSnare': { 'density': 1, 'range': 'mid', 'type': 'percussion'}, 
            'rightPiano': { 'density': 1, 'range': 'mid', 'type': '' },
            'rightPiano2': { 'density': 1, 'range': 'mid', 'type': '' },
            }


        self.MaxAndMinLayersForEnergy = { 
            'high'  : { 'max': 6,  'min': 4, 'initialMax': 5,  'initialMin': 4, 'loRangeMax': 3, 'loRangeMin': 1 }, 
            'medium': { 'max': 4,  'min': 3, 'initialMax': 4,  'initialMin': 3, 'loRangeMax': 1, 'loRangeMin': 1 }, 
            'low'   : { 'max': 3,  'min': 2, 'initialMax': 3,  'initialMin': 2, 'loRangeMax': 2, 'loRangeMin': 1 }, 
            }

        
        self.priorityLoLayers = [ 'bass2' ]
        self.priorityNotLoLayers1 = [ 'rightPiano' ] 
        self.priorityNotLoLayers2 = [ 'drumsKick' ] 



        self.arrange = Arranging ( "BomMarch", self.layers, False ) #useDefault = False 

        # set the initial phrase length
        if ( movement['duration'] <= 45 ) : 
            self.possiblePLs = [ 2 ] 
            self.primaryPL   = random.choice(self.possiblePLs) 
            self.numUniqCPs  = 1 
        elif ( movement['duration'] > 45 and movement['duration'] <= 90 ) : 
            self.possiblePLs = [ 4 ] 
            self.primaryPL   = random.choice(self.possiblePLs) 
            self.numUniqCPs  = 2
        else : 
            self.possiblePLs = [ 4, 4, 3, 4, 5 ] 
            self.primaryPL   = random.choice(self.possiblePLs) 
            self.numUniqCPs  = random.choice ( [ 2, 3, 2 ] ) 


        tonyawards = False

        if ( tonyawards ) : 
            self.numUniqCPs  = 4  
            
        self.minUniqCPs =  1
        self.maxUniqCPs = 7    
        
        if ( self.minUniqCPs > self.maxUniqCPs ) :
            self.maxUniqCPs = self.minUniqCPs
        self.uniqTSEIds = movement['uniqTSEs']      

            
        # set the initail BPM
        self.possibleBPMs = [ x for x in range ( 126, 136, 1) ] 
        self.primaryBPM = random.choice ( self.possibleBPMs ) 
            
        # set the initial scale
        self.possibleKeys = MusicTheory.AllKeys
        self.primaryScale = random.choice ( self.possibleKeys ) 
            
        # set the initial TSE
        if ( self.complexity == 'super_simple' ) : #95 % probability that tse remains same
            self.possibleTSEs = [ '4/4', '3/4', '4/4'  ] 
        elif ( self.complexity == 'simple' ) : #95 % probability that tse remains same
            self.possibleTSEs = [ '2/4', '3/4', '4/4'  ] 
        elif ( self.complexity == 'semi_complex' ) : #90 % probability that tse remains same            
            self.possibleTSEs = [ '3/4', '4/4', '5/4', '7/4', '3/8', '6/8', '7/8' ] 
        elif ( self.complexity == 'complex1' ) : #80 % probability that tse remains same
            self.possibleTSEs = [ '4/4', '5/8', '6/8', '9/8', '11/8', '13/8', '3/16' ]                           

        self.primaryTSE = random.choice ( self.possibleTSEs ) 

        
        if ( 1 ) : 
            print ( "TSE: ", self.primaryTSE ) 
            print ( "BPM: ", self.primaryBPM ) 
            print ( "KEY: ", self.primaryScale ) 
            print ( "PL : ", self.primaryPL )
        
        if ( self.complexity.endswith('simple') ) : 
            self.InitializeMoodForSimple ( movement['sectionSettings'] ) ;
        else : 
            print ( "In the roadmap! Abort!" ) 
            sys.exit(0) 

    def InitializeMoodForSimple ( self, sections ) : 
        
        moodSpecificInfo = { 'fills': True, 'numChords': random.choice([3,4]), 'selectedTempo': self.selectedTempo }
        #self = InitializeSectionsHelper.InitializeSections ( self, sections, moodSpecificInfo ) 
        self = InitializeSectionsHelper.InitializeSectionsComplex ( self, sections, moodSpecificInfo ) 
        #self.keepHalfOfPrevLayers = True

        self = InitializeChordsAndPhraseHelper.InitializeChordsAndPhraseForSections ( self, sections ) 
        
        if ( 1 )  : 
            print() 
            print ( "Arrangement for Movement" ) 
            for secId in self.sections : 
                print ( "Section: ", secId, "Uniq Mel Id: ", self.sections[secId]['melId'], "startingMnum: ", self.sections[secId]['startMNum'], "endMNum: ", self.sections[secId]['endMNum'], 'tse: ', self.sections[secId]['tse'] ) 
                uniqCPId = self.sections[secId]['melId'] 
                numChordsInPhrase = self.uniqCPSettings[uniqCPId]['numChords']
                phNum = 0
                for chId in self.sections[secId]['chords'] : 
                    if ( chId % numChordsInPhrase == 0 ) :
                        print ( "\tPhrase: ", phNum + 1, self.sections[secId]['phrases'][phNum] ) 
                        phNum += 1
                    print ( "\t\tChord: ", chId, self.sections[secId]['chords'][chId] ) 
                print() 

        #sys.exit(0) 



    def setPercussionSettings ( self, tse ) : 
        
        type = 'defaultDrumKitSeparate'
        halfBeats = Constants.TSEBeatInfo[tse]['halfBeats'] 
        strongDownBeats = Constants.TSEBeatInfo[tse]['strongDownBeats'] 
        weakDownBeats = Constants.TSEBeatInfo[tse]['weakDownBeats'] 
        numBeats = Constants.TSEs[tse]['num16thBeats'] 
        oneExtra8thBeatForBassDrumsFilled = False

        BeatInfo = collections.OrderedDict() 

        numBeats = Constants.TSEs[tse]['num16thBeats'] 
        eopStartBeat = numBeats + 1 - random.choice ( [ numBeats//2, numBeats//4 ] )  # end of phrase fill 
        eosStartBeat = numBeats + 1 - random.choice ( [ numBeats, numBeats, numBeats, numBeats//2, numBeats ] )  # end of section fill 
        numPatterns = 1

        patterns = collections.OrderedDict() 
        patterns[0] = { 'eosStartBeat': eosStartBeat, 'eopStartBeat': eopStartBeat }


        if ( 0 ) : 
            print ( "eop: ", eopStartBeat, "eos: ", eosStartBeat ) 


        for i in range ( 1, numBeats+1, 1 ) : 
            
            if ( i in halfBeats ) : 
                BeatInfo[i] = { 
                    'kick' :   { 'probMax': 90, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'snare':   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    'hihat':   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    'bass' :   { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 70 }, 
                    }

            elif ( i in strongDownBeats ) : 
                
                BeatInfo[i] = { 
                    'kick' :   { 'probMax': 90, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'snare':   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    'hihat':   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    'bass' :   { 'probMax': 50, 'probMin': 30, 'velocityMax': 120, 'velocityMin': 70 }, 
                    }


            elif ( i in weakDownBeats ) : 
                
                BeatInfo[i] = { 
                    'kick' :   { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'snare':   { 'probMax': 90, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'hihat':   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    'bass' :   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    }
                                            
            else : 
                
                BeatInfo[i] = { 
                    'kick' :   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    'snare':   { 'probMax': 30, 'probMin': 0,  'velocityMax': 80,  'velocityMin': 60 }, 
                    'hihat':   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    'bass' :   { 'probMax': 0,  'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    }
            

        return BeatInfo, patterns, type


