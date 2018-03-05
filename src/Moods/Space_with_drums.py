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

class Space_with_drums : 

    def __init__ ( self, movement, selectedTempo ) : 

        self.complexity = movement['complexity'] 
        self.durationInSecs = movement['duration'] 
        self.rhythmSpeed = movement['rhythmSpeed']
        self.selectedTempo = selectedTempo 


        self.groupLayers = {
            'rhythm': { 'layers': [ 'bass3',  'drumsKit', 'rightPiano', 'brassRhythms' ] , 'heavy': 4, 'lite': 2, 'medium': 3 } , 
            'melody': { 'layers': [ 'mel5' ],  'heavy': 1, 'lite': 1, 'medium': 1 } , 
            }

        self.layers = {      
            'bass1': { 'density': 1, 'range': 'low', 'type': '' },
            #'bass2': { 'density': 1, 'range': 'low', 'type': '' },
            #'bass3': { 'density': 1, 'range': 'low', 'type': '' },

            'arpStrings':   { 'density': 1, 'range': 'mid', 'type': 'strings' }, 
            #'brassRhythms': { 'density': 1, 'range': 'mid', 'type': 'rhythm' },           
            'rightPiano':   { 'density': 1, 'range': 'mid', 'type': '' },
            'rightPiano2':  { 'density': 1, 'range': 'mid', 'type': '' },
            'leftPianoBass': { 'density': 1, 'range': 'low', 'type': '' },
            'piano1':  { 'density': 1, 'range': 'all', 'type': '' },
            #'rhythmChords': { 'density': 1, 'range': 'mid', 'type': '' },
            #'midStrings':   { 'density': 1, 'range': 'mid', 'type': 'strings' },
            #'drumsSnare': { 'density': 1, 'range': 'mid', 'type': 'percussion' },
            'drumsBass': { 'density': 1, 'range': 'low', 'type': 'percussion' },

            'mel5': { 'density': 1, 'range': 'midToHi', 'type': '' }, 
            'hiStrings': { 'density': 1, 'range': 'hi', 'type': 'strings' },

            }
        
        self.MaxAndMinLayersForEnergy = { 
            'high'  : { 'max': 11,  'min': 1, 'initialMax': 9,  'initialMin': 6, 'loRangeMax': 4, 'loRangeMin': 1 }, 
            'medium': { 'max': 11,   'min': 1, 'initialMax': 5,  'initialMin': 3, 'loRangeMax': 3, 'loRangeMin': 1 }, 
            'low'   : { 'max': 11,   'min': 1, 'initialMax': 3,  'initialMin': 1, 'loRangeMax': 2, 'loRangeMin': 0 }, 
            }
        

        self.arrange = Arranging ( "Space_with_drums", self.layers, False ) #useDefault = False 

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
        self.possibleBPMs = [ x for x in range ( 114, 124, 1) ] 
        self.primaryBPM = random.choice ( self.possibleBPMs ) 
            
        # set the initial scale
        self.possibleKeys = MusicTheory.AllKeys
        self.primaryScale = random.choice ( self.possibleKeys ) 

        # set the initial TSE
        if ( self.complexity == 'super_simple' ) : #95 % probability that tse remains same
            self.possibleTSEs = [ '4/4'  ] 
            self.maxUniqCPs = 2
        elif ( self.complexity == 'simple' ) : #95 % probability that tse remains same
            self.possibleTSEs = [ '4/4'  ] 
            self.maxUniqCPs = 2
        elif ( self.complexity == 'semi_complex' ) : #90 % probability that tse remains same            
            self.possibleTSEs = [ '3/4', '4/4', '5/4', '7/4', '3/8', '6/8', '7/8' ] 
            random.shuffle( self.possibleTSEs ) 
            self.possibleTSEs = [ self.possibleTSEs[0], self.possibleTSEs[1] ] 
            self.maxUniqCPs = 3
        elif ( self.complexity == 'complex1' ) : #80 % probability that tse remains same
            self.possibleTSEs = [ '4/4', '5/8', '6/8', '9/8', '11/8', '13/8', '3/16' ]                           
            random.shuffle( self.possibleTSEs ) 
            self.possibleTSEs = [ self.possibleTSEs[0], self.possibleTSEs[1], self.possibleTSEs[2] ] 
            self.maxUniqCPs = 4

        self.primaryTSE = random.choice ( self.possibleTSEs ) 

        self.minUniqCPs =  len(movement['uniqTSEs'])
        if ( self.minUniqCPs > self.maxUniqCPs ) :
            self.maxUniqCPs = self.minUniqCPs
        self.uniqTSEIds = movement['uniqTSEs']

        
        if ( 1 ) : 
            print ( "TSE: ", self.primaryTSE ) 
            print ( "BPM: ", self.primaryBPM ) 
            print ( "KEY: ", self.primaryScale ) 
            print ( "PL : ", self.primaryPL )


        movement['sectionSettings'][0]['bassRhythmType'] = 'popRhythms' 

        self.InitializeMoodForSimple ( movement['sectionSettings'] ) ;



        
    def setChordProgressions ( self ) : 
        
        return 

    def InitializeMoodForSimple ( self, sections ) :
        
        moodSpecificInfo = { 'fills':  True, 'numChords': random.choice([3,4]), 'selectedTempo': self.selectedTempo }
        self = InitializeSectionsHelper.InitializeSectionsComplex ( self, sections, moodSpecificInfo ) 

        if ( 0 ) : 
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
        
        type = 'defaultDrumKit'
        middleBeats = Constants.TSEBeatInfo[tse]['middleBeats'] 
        halfBeats = Constants.TSEBeatInfo[tse]['halfBeats'] 
        strongDownBeats = Constants.TSEBeatInfo[tse]['strongDownBeats'] 
        weakDownBeats = Constants.TSEBeatInfo[tse]['weakDownBeats'] 
        backBeat = Constants.TSEBeatInfo[tse]['backBeat']
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


        maxUpBeats = 2
        numUpBeatsForKick = 0 
        numUpBeatsForSnare = 0 
        numUpBeatsForHihat = 0 


        beatArray = [ i for i in range ( 1, numBeats+1, 1 ) ]
        #print ( "Beat Array: ", beatArray ) 
        random.shuffle ( beatArray ) 
        #print ( "Beat Array: ", beatArray ) 


        #for i in range ( 1, numBeats+1, 1 ) : 
        for i in beatArray :
         
         
            if ( i in backBeat ) : 
                    
                BeatInfo[i] = { 
                    'kick' :   { 'probMax': 50, 'probMin': 40, 'velocityMax': 110, 'velocityMin': 80 }, 
                    'lowDkick' :   { 'probMax': 0, 'probMin': 0, 'velocityMax': 100, 'velocityMin': 70 }, 
                    'snare':   { 'probMax': 95, 'probMin': 95,  'velocityMax': 125,  'velocityMin': 110 }, 
                    'lowDsnare':   { 'probMax': 95, 'probMin': 95, 'velocityMax': 110, 'velocityMin': 100 }, 
                    'hihat':   { 'probMax': 80, 'probMin': 60, 'velocityMax': 90,  'velocityMin': 60 }, 
                    'lowDhihat':   { 'probMax': 10, 'probMin': 10, 'velocityMax': 80,  'velocityMin': 50 }, 
                    'bass' :   { 'probMax': 0, 'probMin': 0, 'velocityMax': 120, 'velocityMin': 70 }, 
                    }

            elif ( i in strongDownBeats ) : 
                
                BeatInfo[i] = { 
                    'kick' :   { 'probMax': 90, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'lowDkick' :   { 'probMax': 80, 'probMin': 60, 'velocityMax': 90, 'velocityMin': 70 }, 
                    'snare':   { 'probMax': 40, 'probMin': 20, 'velocityMax': 110, 'velocityMin': 80 }, 
                    'lowDsnare':   { 'probMax': 30, 'probMin': 20, 'velocityMax': 80, 'velocityMin': 50 }, 
                    'hihat':   { 'probMax': 85, 'probMin': 65, 'velocityMax': 100, 'velocityMin': 80 }, 
                    'lowDhihat':   { 'probMax': 10, 'probMin': 10, 'velocityMax': 80,  'velocityMin': 50 }, 
                    'bass' :   { 'probMax': 80, 'probMin': 10, 'velocityMax': 100, 'velocityMin': 70 }, 
                    }         

         
            elif ( i in middleBeats ) : 
                BeatInfo[i] = { 
                    'kick' :       { 'probMax': 30, 'probMin': 15, 'velocityMax': 100, 'velocityMin': 70 }, 
                    'lowDkick' :   { 'probMax': 0, 'probMin': 0, 'velocityMax': 110, 'velocityMin': 70 }, 
                    'snare':       { 'probMax': 10, 'probMin': 0, 'velocityMax': 50, 'velocityMin': 20 }, 
                    'lowDsnare':   { 'probMax': 70, 'probMin': 60, 'velocityMax': 100, 'velocityMin': 70 }, 
                    'hihat':       { 'probMax': 90, 'probMin': 70, 'velocityMax': 100, 'velocityMin': 85 }, 
                    'lowDhihat':   { 'probMax': 20, 'probMin': 10, 'velocityMax': 80,  'velocityMin': 50 }, 
                    'bass' :   { 'probMax': 0, 'probMin': 0, 'velocityMax': 120, 'velocityMin': 70 }, 
                    }
            
            
            elif ( i in halfBeats ) : 
                BeatInfo[i] = { 
                    'kick' :       { 'probMax': 85, 'probMin': 75, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'lowDkick' :   { 'probMax': 0, 'probMin': 0, 'velocityMax': 110, 'velocityMin': 70 }, 
                    'snare':       { 'probMax': 20, 'probMin': 10, 'velocityMax': 80,  'velocityMin': 40 }, 
                    'lowDsnare':   { 'probMax': 25, 'probMin': 15, 'velocityMax': 50, 'velocityMin': 40 }, 
                    'hihat':       { 'probMax': 90, 'probMin': 70, 'velocityMax': 110, 'velocityMin': 90 }, 
                    'lowDhihat':   { 'probMax': 20, 'probMin': 10, 'velocityMax': 80,  'velocityMin': 50 }, 
                    'bass' :       { 'probMax': 0, 'probMin': 0, 'velocityMax': 120, 'velocityMin': 70 }, 
                    }





            elif ( i in weakDownBeats ) : 
                    
                BeatInfo[i] = { 
                    'kick' :   { 'probMax': 70, 'probMin': 50, 'velocityMax': 120, 'velocityMin': 70 }, 
                    'lowDkick' :   { 'probMax': 0, 'probMin': 0, 'velocityMax': 90, 'velocityMin': 70 }, 
                    'snare':   { 'probMax': 25, 'probMin': 5,  'velocityMax': 60,  'velocityMin': 30 }, 
                    'lowDsnare':   { 'probMax': 30, 'probMin': 20, 'velocityMax': 80, 'velocityMin': 50 }, 
                    'hihat':   { 'probMax': 80, 'probMin': 60, 'velocityMax': 90,  'velocityMin': 60 }, 
                    'lowDhihat':   { 'probMax': 10, 'probMin': 10, 'velocityMax': 80,  'velocityMin': 50 }, 
                    'bass' :   { 'probMax': 0, 'probMin': 0, 'velocityMax': 120, 'velocityMin': 70 }, 
                    }
            
                                            
            else : 
                
                if ( numUpBeatsForKick < maxUpBeats and random.randint (0, 100 ) < 70 ) : 
                    probMaxKick = 70 
                    numUpBeatsForKick += 1
                else :
                    probMaxKick = 0 


                if ( numUpBeatsForSnare < maxUpBeats and random.randint (0, 100 ) < 70 ) : 
                    probMaxSnare = 70 
                    numUpBeatsForSnare += 1
                else :
                    probMaxSnare = 0 


                if ( numUpBeatsForHihat < maxUpBeats and random.randint (0, 100 ) < 70 ) : 
                    probMaxHihat = 70 
                    numUpBeatsForHihat += 1
                else :
                    probMaxHihat = 0 

                BeatInfo[i] = { 
                    'kick' :   { 'probMax': probMaxKick,  'probMin': 10, 'velocityMax': 80,  'velocityMin': 60 }, 
                    'lowDkick' :   { 'probMax': 5, 'probMin': 1, 'velocityMax': 90, 'velocityMin': 70 }, 
                    'snare':   { 'probMax': probMaxSnare, 'probMin': 0,  'velocityMax': 50,  'velocityMin': 20 }, 
                    'lowDsnare':   { 'probMax': 0, 'probMin': 0, 'velocityMax': 80, 'velocityMin': 50 }, 
                    'hihat':   { 'probMax': probMaxHihat, 'probMin': 10, 'velocityMax': 60,  'velocityMin': 40 }, 
                    'lowDhihat':   { 'probMax': 0, 'probMin': 00, 'velocityMax': 80,  'velocityMin': 50 }, 
                    'bass' :   { 'probMax': 0,            'probMin': 0,  'velocityMax': 0,   'velocityMin': 0 }, 
                    }
            
        #sys.exit(0) 
        return BeatInfo, patterns, type

