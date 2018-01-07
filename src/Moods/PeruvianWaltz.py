from __future__ import print_function
from Skeleton import MusicTheory
from Skeleton import Constants
from Arranging.Arranging import *
import InitializeSectionsHelper
import InitializeChordsAndPhraseHelper

import sys
import math
import random
import collections

class PeruvianWaltz : 

    def __init__ ( self, movement ) : 

        self.complexity = movement['complexity'] 
        self.durationInSecs = movement['duration'] 
        self.rhythmSpeed = movement['rhythmSpeed'] 
        if ( 0 ) : 
            print ( "Mood: Peruvian Waltz" ) 
            print ( 'Complexity: ', self.complexity ) 

        self.percussionDesc = ['drumsKitMarinera']

        self.layers = {
            'bass1': { 'density': 1, 'range': 'low', 'type': '' },
            'bass2': { 'density': 1, 'range': 'low', 'type': '' },
            'loStrings': { 'density': 1, 'range': 'low', 'type': 'strings' },
            'leftPianoBass': { 'density': 1, 'range': 'low', 'type': '' },


            'rightPiano': { 'density': 1, 'range': 'mid', 'type': '' },
            'peruvianRhythmChords': { 'density': 1, 'range': 'mid', 'type': '' },
            'rhythmChords': { 'density': 1, 'range': 'mid', 'type': '' },
            'midStrings': { 'density': 1, 'range': 'mid', 'type': 'strings' },
            'drumsKitMarinera' : { 'density': 1, 'range': 'mid', 'type': 'percussion' },

            'arpStrings': { 'density': 1, 'range': 'midToHi', 'type': 'strings' }, 
            'mel5': { 'density': 1, 'range': 'midToHi', 'type': '' }, 

            'hiStrings': { 'density': 1, 'range': 'hi', 'type': 'strings' },
            'piano1':  { 'density': 1, 'range': 'hi', 'type': '' },
            }    

        self.notLoLayers = {
            'rightPiano': { 'density': 1, 'range': 'mid', 'type': '' },
            'rhythmChords': { 'density': 1, 'range': 'mid', 'type': '' },
            'peruvianRhythmChords': { 'density': 1, 'range': 'mid', 'type': '' },
            'midStrings': { 'density': 1, 'range': 'mid', 'type': 'strings' },
            'drumsKitMarinera' : { 'density': 1, 'range': 'mid', 'type': 'percussion' },
            
            'arpStrings': { 'density': 1, 'range': 'midToHi', 'type': 'strings' }, 
            'mel5': { 'density': 1, 'range': 'midToHi', 'type': '' }, 
            
            'hiStrings': { 'density': 1, 'range': 'hi', 'type': 'strings' },
            'piano1':  { 'density': 1, 'range': 'hi', 'type': '' },
            }
        

        self.percussionType = 'Marinera'

        self.MaxAndMinLayersForEnergy = { 
            'high'  : { 'max': 11, 'min': 6, 'initialMax': 9,  'initialMin': 8, 'loRangeMax': 4, 'loRangeMin': 2 }, 
            'medium': { 'max': 7,  'min': 3, 'initialMax': 6,  'initialMin': 4, 'loRangeMax': 3, 'loRangeMin': 2 }, 
            'low'   : { 'max': 4,  'min': 2, 'initialMax': 4,  'initialMin': 2, 'loRangeMax': 3, 'loRangeMin': 1 }, 
            }
        

        self.priorityLoLayers = [] 
        self.priorityNotLoLayers1 = [ 'peruvianRhythmChords' ] 
        self.priorityNotLoLayers2 = [ 'drumsKitMarinera' ]

        self.arrange = Arranging ( "PeruvianWaltz", self.layers, False ) #useDefault = False 

        # set the initial phrase length
        if ( movement['duration'] <= 45 ) : 
            self.possiblePLs = [ 4 ] 
            self.primaryPL   = random.choice(self.possiblePLs) 
            self.numUniqCPs  = 1 
        elif ( movement['duration'] > 45 and movement['duration'] <= 90 ) : 
            self.possiblePLs = [ 4 ] 
            self.primaryPL   = random.choice(self.possiblePLs) 
            self.numUniqCPs  = 2
        else : 
            self.possiblePLs = [ 4 ] 
            self.primaryPL   = random.choice(self.possiblePLs) 
            self.numUniqCPs  = random.choice ( [ 2, 3, 2 ] ) 

            
        # set the initail BPM
        self.possibleBPMs = [ x for x in range ( 100, 130, 1) ] 
        self.primaryBPM = random.choice ( self.possibleBPMs ) 
            
        # set the initial scale
        self.possibleKeys = MusicTheory.AllKeys
        self.primaryScale = random.choice ( self.possibleKeys ) 
            
        # set the initial TSE
        
        if ( self.complexity == 'super_simple' ) : #95 % probability that tse remains same
            self.possibleTSEs = [ '3/4' ] 
        elif ( self.complexity == 'simple' ) : #95 % probability that tse remains same
            self.possibleTSEs = [ '3/4'  ] 
        elif ( self.complexity == 'semi_complex' ) : #90 % probability that tse remains same            
            self.possibleTSEs = [ '3/4', '6/4' ] 
        elif ( self.complexity == 'complex1' ) : #80 % probability that tse remains same
            self.possibleTSEs = [ '3/4', '6/4', '7/4' ] 

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

        #self.setChordProgressions ( ) 
        #sys.exit(0) 

        
    def setChordProgressions ( self ) : 
        
        return 

    def InitializeMoodForSimple ( self, sections ) :
        
        moodSpecificInfo = { 'fills':  False, 'numChords': self.primaryPL }
        self = InitializeSectionsHelper.InitializeSections ( self, sections, moodSpecificInfo ) 
        self.keepHalfOfPrevLayers = True

        if ( 1 ) : 
            for secId in self.sections :         
                print ( "Id", secId, "startMNum: ", self.sections[secId]['startMNum'], "endMNum: ", self.sections[secId]['endMNum'], 'Mel Id: ', self.sections[secId]['melId']  ) 

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

    def setPercussionSettings ( self, tse ) : 

        numBeats = Constants.TSEs[tse]['num16thBeats'] 
        if ( tse == '3/4' ) : 
            hiBeats = [ 1, 4, 7, 11]
            loBeats = [ 3, 5, 9 ]            
            type = 'peruvianMarinera'
        elif ( tse == '6/4' ) : 
            hiBeats = [ 5, 15, 21 ] 
            loBeats = [ 1, 9, 11, 17, 23 ] 
            type = 'peruvianLando'
        else : 
            type = 'defaultDrumKit'
            hiBeats = [ i for i in range ( 1, numBeats+1, 2 ) ] 
            loBeats = [ i for i in range ( 0, numBeats, 2 ) ] 
            probMax = 80
            probMin = 50 
            
        BeatInfo = collections.OrderedDict() 

        # no fills for peruvian waltz
        #eopStartBeat = numBeats + 1 - random.choice ( [ numBeats//2, numBeats//4 ] )  # end of phrase fill 
        #eosStartBeat = numBeats + 1 - random.choice ( [ numBeats, numBeats, numBeats, numBeats//2, numBeats ] )  # end of section fill 
        numPatterns = 1

        eopStartBeat = numBeats + 1
        eosStartBeat = numBeats + 1

        patterns = collections.OrderedDict() 
        patterns[0] = { 'eosStartBeat': eosStartBeat, 'eopStartBeat': eopStartBeat }

        if ( 0 ) : 
            print ( "eop: ", eopStartBeat, "eos: ", eosStartBeat ) 

        beatArray = [ i for i in range ( 1, numBeats+1, 1 ) ]
        #print ( "Beat Array: ", beatArray ) 
        random.shuffle ( beatArray ) 
        #print ( "Beat Array: ", beatArray ) 


        for i in beatArray :
         
            if ( i in hiBeats ) : 
                BeatInfo[i] = { 
                    'hiBeat' :   { 'probMax': 90, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'loBeat' :   { 'probMax': 0,  'probMin': 0,  'velocityMax': 110, 'velocityMin': 70 }, 
                    }
            
            elif ( i in loBeats ) : 
                BeatInfo[i] = { 
                    'hiBeat' :   { 'probMax': 0,  'probMin': 0,  'velocityMax': 120, 'velocityMin': 70 }, 
                    'loBeat' :   { 'probMax': 90, 'probMin': 80, 'velocityMax': 110, 'velocityMin': 70 }, 
                    }

            else : 
                BeatInfo[i] = { 
                    'hiBeat' :   { 'probMax': 0,  'probMin': 0,  'velocityMax': 120, 'velocityMin': 70 }, 
                    'loBeat' :   { 'probMax': 0,  'probMin': 0,  'velocityMax': 110, 'velocityMin': 70 }, 
                    }
            
        #sys.exit(0) 
        return BeatInfo, patterns, type

