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

import Melody5
import Constants
import MidiOutput
import Pentatonic
import LayerFills
import MusicTheory
import learnDJWMelody
import AccompanyingLayers
import ExtractMidiTrainingData

from Percussions import Percussions

class Section: 
    
    def __init__ ( self, wbLevers, midiFile ) :
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
        self.midiFile = midiFile
        
        # Intitialize the default bass layer 
        self.bass1Obj = Bass1.Bass1 ( self.wbLevers ) 

        # Initialize the bass1 rhythm for the section.
        self.rhy = Rhythm.Rhythm ( wbLevers )   # wbLevers['bassRhy'] gives the chord durations for the bass

        self.numChords = len(self.rhy.ChordDurations) 
        self.layers = collections.OrderedDict()          
               
    
    def PrintClassInfo ( self ) : 
        print() 
        print ( "WB Levers:" , self.wbLevers ) 
        self.bass1Obj.PrintClassInfo () 
        

    def run ( self ) :         

        self.layers['bass1'] = self.bass1Obj.run ( self.rhy.ChordDurations )         

        # needed for dj watson melody
        self.chordDict = collections.OrderedDict() 
        phraseNum = 0 
        for chordId in range(self.numChords) : 
            self.chordDict[chordId] = { 'duration': self.bass1Obj.Chords[phraseNum][chordId][0]['duration'][0], 'chord': self.bass1Obj.Chords[phraseNum][chordId][0]['chord'], 'scale':  self.bass1Obj.Chords[phraseNum][chordId][0]['scale'] } 

        # Initialize and run Melody 5 layer
        self.layers['mel5'] = self.initializeAndRunDJWatsonMelody () 


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


        return self.layers
        

    def initializeAndRunDJWatsonMelody ( self ) :
        
        self.mel5Objs = [] 
        trainedData = collections.OrderedDict() 
        mel5TrainedData = []

        chords = []
        scales = []
        ids    = [] 
        durations = [] 
        total = 0

        for chordId in range(self.numChords) :
            ids.append ( chordId ) 
            chords.append ( self.chordDict[chordId]['chord'] ) 
            scales.append ( self.chordDict[chordId]['scale'] )
            durations.append ( self.chordDict[chordId]['duration'] ) 


        if ( 1 ) : 
            print ( "-------------------------------- DJ MEL Starts --------------------------------------" ) 
            print() 


        if ( 0 ) : 
            print  ( "Ids: ", ids, "Chords: ", chords, "Scales: ", scales, "Chord Durations: ", durations ) 

        
        # setting the training data for the RBM based on midi file input
        cmd = "python mididump.py {}  > midi_export.mid.dump".format( self.midiFile )
        print ( "Mididump Command: ", cmd ) 
        os.system ( cmd ) 

        midiTrainingData = ExtractMidiTrainingData.MidiTrainingData (  "midi_export.mid.dump" ) 
        os.system( "rm midi_export.mid.dump" )

        midiTrainingData.ExtractChords ( chords, scales, durations ) 


        phraseNum = 0 
        # mel5Data structure: Dictionary of Dictionary of lists.
        # 1st dictionary is for phrase
        # 2nd dictinary is for chord in phrase
        # list is for item in phrase and chord
        self.mel5Data = collections.OrderedDict()  # collection of Phrases
        self.mel5Data[phraseNum] = collections.OrderedDict()  # collection of chords within phrase


        itemsForOctaveBalancing = [] 

        for chId in midiTrainingData.melody :
            if ( 0 ) :
                print ( "Chord: ", chId ) 

            if ( chords[chId] not in MusicTheory.KeyDict ) :
                scale = scales[chId] 
            else :
                scale = chords[chId]
            tr_pitch     = []
            tr_startTime = []
            tr_endTime   = []
            new_pitch    = []
            tr_scale     = []
            tr_chord     = []

            for item in midiTrainingData.melody[chId] :
                tr_pitch.append ( item['pitch'] / 100.0 ) 
                tr_startTime.append ( item['Clk'][0] ) 
                tr_endTime.append ( item['Clk'][1] ) 
                tr_scale.append ( scale )
                tr_chord.append ( chords[chId] ) 

            total += self.chordDict[chId]['duration']                 

            new_pitch  = learnDJWMelody.run ( tr_pitch, tr_startTime, tr_endTime, scale )
            self.mel5Data[phraseNum][chId] = [] 


            if ( 0 ) :
                print ( "chord Id: ", chId ) 
                print ( "Old Pitch : ", tr_pitch ) 
                print ( "New Pitch : ", new_pitch ) 
                print ( "Start Time: ", tr_startTime ) 
                print ( "End Time  : ", tr_endTime ) 
                print () 

                
            for item in range(len(new_pitch)) : 

                if ( 0 ) : 
                    print ( "Item: ", item, new_pitch[item], tr_startTime[item] , tr_endTime[item]  ) 

                note = MusicTheory.pitchToNotes[new_pitch[item]%12]
                #self.mel5Data[phraseNum][chId].append ( { 'chord': tr_chord[item], 'scale' : tr_scale[item], 'duration': [ tr_endTime[item] - tr_startTime[item] ], 'velocity': [ random.randint(50, 80) ], 'pitches': [ new_pitch[item] ] , 'notes': [ note ], 'Clk': [ tr_startTime[item], tr_endTime[item] ]  } )
                itemsForOctaveBalancing.append (  { 'chordId': chId, 'chord': tr_chord[item], 'scale' : tr_scale[item], 'duration': [ tr_endTime[item] - tr_startTime[item] ], 'velocity': [ random.randint(50, 80) ], 'pitches': [ new_pitch[item] ] , 'notes': [ note ], 'Clk': [ tr_startTime[item], tr_endTime[item] ]  } )

                continue

                if ( item+1 < len(new_pitch) and tr_endTime[item] < tr_startTime[item+1] ) :
                    self.mel5Data[phraseNum][chId].append ( {'nullNote': True, 'chord': tr_chord[item], 'scale' : tr_scale[item], 'duration': [ tr_startTime[item+1] - tr_endTime[item] ], 'velocity': [ 0 ], 'pitches': [ new_pitch[item] ] , 'notes': [ note ], 'Clk': [  tr_endTime[item], tr_startTime[item+1] ]  } )
                    itemsForOctaveBalancing.append (  {'nullNote': True, 'chord': tr_chord[item], 'scale' : tr_scale[item], 'duration': [ tr_startTime[item+1] - tr_endTime[item] ], 'velocity': [ 0 ], 'pitches': [ new_pitch[item] ] , 'notes': [ note ], 'Clk': [  tr_endTime[item], tr_startTime[item+1] ]  } )
                    #print ( "I am here 1" )
                
                elif ( item+1 < len(new_pitch) and tr_endTime[item] > tr_startTime[item+1] ) :
                    if ( 0 ) :
                        print ( "Do Nothing" ) 

                elif ( tr_endTime[item] != total ) : 
                    self.mel5Data[phraseNum][chId].append ( {'nullNote': True, 'chord': tr_chord[item], 'scale' : tr_scale[item], 'duration': [ total - tr_endTime[item] ], 'velocity': [ 0 ], 'pitches': [ new_pitch[item] ] , 'notes': [ note ], 'Clk': [  tr_endTime[item], total ]  } )
                    itemsForOctaveBalancing.append (  {'nullNote': True, 'chord': tr_chord[item], 'scale' : tr_scale[item], 'duration': [ total - tr_endTime[item] ], 'velocity': [ 0 ], 'pitches': [ new_pitch[item] ] , 'notes': [ note ], 'Clk': [  tr_endTime[item], total ]  } )

                    #print ( "I am here 2" ) 



        if ( 0 ) : 
            for itemIndex, item in enumerate(itemsForOctaveBalancing) : 
                print ( itemIndex, item['pitches'][0], item['velocity'][0] ) 
                                          

        # balance octaves
        itemCnt = 0 
        numItems = len(itemsForOctaveBalancing) 
        firstItem = True
        while itemCnt < numItems : 
            item = itemsForOctaveBalancing[itemCnt] 

            if ( 0 ) : 
                print() 
                print ( "ItemCnt : ", itemCnt, item )  

            currPitch = itemsForOctaveBalancing[itemCnt]['pitches'][0] 
            if ( firstItem ) : 
                prevPitch = itemsForOctaveBalancing[itemCnt]['pitches'][0] 
                cumulativeStep = 0 
                currStep = 0
                itemCnt += 1
                firstItem = False
                maxPitch = prevPitch + 24
                minPitch = prevPitch - 12
                continue
            else :                 
                if ( currPitch > prevPitch ) : 
                    if ( 0 ) : 
                        print ( "Here : 1: currPitch ", currPitch , " > " , prevPitch, " prevPitch " ) 
                    currStep = currPitch - prevPitch 
                    if ( cumulativeStep + currStep > 10 or currStep > 8 ) : 
                        if ( 0 ) : 
                            print ( "Here : 1a cumSt + cstep > 10 or cstep >= 8, cumulativeStep : ", cumulativeStep, " currStep: ", currStep ) 
                        currItemToCheck = currPitch - 12
                        itemToCheck = itemCnt - 1 
                        itemForBalancingFound = False
                        while ( itemToCheck >= 0 ) : 
                            prevItemToCheck = itemsForOctaveBalancing[itemToCheck]['pitches'][0] 
                            if ( prevItemToCheck - currItemToCheck  < 10 ) : 
                                itemForBalancingFound = True
                                break 
                            else : 
                                currItemToCheck = prevItemToCheck - 12 
                                itemToCheck -= 1
                        if ( not itemForBalancingFound ) :   # no item found for balancing. make this a rest note
                            itemsForOctaveBalancing[itemCnt]['velocity'][0] = 0 
                            if ( 0 ) : 
                                print ( "Here : 1b, no pitch found for balancing, itemCnt: ", itemCnt, "item: ", itemsForOctaveBalancing[itemCnt] ) 
                            itemCnt += 1 ;
                            continue
                        else : 
                            if ( 0 ) : 
                                print ( "Here : 1c Item Found for balancing: ", itemToCheck+1, "Before balancing: ", itemsForOctaveBalancing[itemToCheck+1], "diff: " ) 
                            cntUp = 0 
                            while ( cntUp < 2  ) : 
                                itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] -= 12  
                                cntUp += 1
                                if ( abs( itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] - itemsForOctaveBalancing[itemToCheck]['pitches'][0] ) <= 10 ) : 
                                    break 
                            if ( 0 ) : 
                                print ( "Here : 1c Item Found for balancing: ", itemToCheck+1, "After balancing: ", itemsForOctaveBalancing[itemToCheck+1] ) 


                            if ( itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] < minPitch ) :                                 
                                itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] += 12
                                if ( 0 ) : 
                                    print ( "Here : 1d Item less than min pitch. Increase by octave: ", itemToCheck+1, "After Increasing by octave: ", itemsForOctaveBalancing[itemToCheck+1] ) 

                            cumulativeStep = itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] - itemsForOctaveBalancing[0]['pitches'][0] 
                            prevPitch = itemsForOctaveBalancing[itemToCheck+1]['pitches'][0]
                            itemCnt = itemToCheck + 1 + 1 
                            if ( 0 ) : 
                                print ( "Next Item to check: ", itemCnt, "Cumulative STep: ", cumulativeStep ) 
                            continue

                    else : # for if ( cumulativeStep + currStep > 10 or currStep >= 8 ) : 
                        if ( 0 ) : 
                            print ( "Here : 1e cumSt + cstep <= 10 and cstep < 8, cumulativeStep : ", cumulativeStep, " currStep: ", currStep ) 
                        cumulativeStep += currStep
                        prevPitch = currPitch
                        itemCnt += 1
                        continue
                elif ( currPitch < prevPitch ) : 
                    if ( 0 ) : 
                        print ( "Here : 2: currPitch ", currPitch , " < " , prevPitch, " prevPitch " ) 

                    currStep = currPitch - prevPitch 
                    if ( cumulativeStep + currStep < -10 or currStep < -8 ) : 
                        if ( 0 ) : 
                            print ( "Here : 2a cumSt + cstep < -10 or cstep <= -8, cumulativeStep : ", cumulativeStep, " currStep: ", currStep ) 

                        currItemToCheck = currPitch + 12

                        itemToCheck = itemCnt - 1 
                        itemForBalancingFound = False
                        while ( itemToCheck >= 0 ) : 
                            prevItemToCheck = itemsForOctaveBalancing[itemToCheck]['pitches'][0] 
                            if ( prevItemToCheck - currItemToCheck  > -10 ) : 
                                itemForBalancingFound = True
                                break 
                            else : 
                                currItemToCheck = prevItemToCheck + 12 
                                itemToCheck -= 1
                        if ( not itemForBalancingFound ) :   # no item found for balancing. make this a rest note
                            if ( 0 ) : 
                                print ( "Here : 2b, no pitch found for balancing, itemCnt: ", itemCnt, "item: ", itemsForOctaveBalancing[itemCnt] ) 
                            itemsForOctaveBalancing[itemCnt]['velocity'][0] = 0 
                            itemCnt += 1 ;
                            continue
                        else : 
                            if ( 0 ) : 
                                print ( "Here : 2c Item Found for balancing: ", itemToCheck+1, "Before balancing: ", itemsForOctaveBalancing[itemToCheck+1] ) 
                            cntUp = 0 
                            while ( cntUp < 2  ) : 
                                itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] += 12
                                cntUp += 1
                                if ( abs( itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] - itemsForOctaveBalancing[itemToCheck]['pitches'][0] ) <= 10 ) : 
                                    break 

                            if ( 0 ) : 
                                print ( "Here : 2c Item Found for balancing: ", itemToCheck+1, "After balancing: ", itemsForOctaveBalancing[itemToCheck+1] ) 

                            if ( itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] > maxPitch ) : 
                                itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] -= 12
                                if ( 0 ) :
                                    print ( "Here : 2d Item greater than man pitch. Decrease by octave: ", itemToCheck+1, "After Decreasing by octave: ", itemsForOctaveBalancing[itemToCheck+1] ) 
                            prevPitch = itemsForOctaveBalancing[itemToCheck+1]['pitches'][0]
                            cumulativeStep = itemsForOctaveBalancing[itemToCheck+1]['pitches'][0] - itemsForOctaveBalancing[0]['pitches'][0] 
                            itemCnt = itemToCheck + 1 + 1 
                            if ( 0 ) : 
                                print ( "Next Item to check: ", itemCnt, "Cumulative STep: ", cumulativeStep ) 
                            continue

                    else : # for if ( cumulativeStep + currStep < -10 or currStep <= -8 ) : 
                        if ( 0 ) : 
                            print ( "Here : 2e cumSt + cstep >= 10 and cstep > -8, cumulativeStep : ", cumulativeStep, " currStep: ", currStep ) 
                        cumulativeStep += currStep
                        prevPitch = currPitch
                        itemCnt += 1
                        continue
                    
                elif ( currPitch == prevPitch ) : 
                    if ( 0 ) : 
                        print ( "Here : 2: currPitch ", currPitch , " == " , prevPitch, " prevPitch " ) 

                    prevPitch = currPitch
                    itemCnt += 1
                    continue
                    



        if ( 0 ) : 
            print() 
            for itemIndex, item in enumerate(itemsForOctaveBalancing) : 
                if ( itemIndex > 0 ) : 
                    print ( itemIndex, "Pitch: ", item['pitches'][0], "diff: " , abs(itemsForOctaveBalancing[itemIndex-1]['pitches'][0] -  itemsForOctaveBalancing[itemIndex]['pitches'][0] ), item['duration'][0],  item['notes'][0] ) 
                else : 
                    print ( itemIndex, "Pitch: ", item['pitches'][0], "diff: " , 0, item['duration'][0],  item['notes'][0] ) 



        itemsForOctaveBalancing = self.fixOctaves ( itemsForOctaveBalancing ) 

        #sys.exit(0) 
                
        
        for item in range(len(itemsForOctaveBalancing) ) : 

            chId = itemsForOctaveBalancing[item]['chordId']             
            self.mel5Data[phraseNum][chId].append ( itemsForOctaveBalancing[item] ) 
            
            if ( item + 1 >= len(itemsForOctaveBalancing) ) : 
                
                if ( itemsForOctaveBalancing[item]['Clk'][1] < total ) : 
                    newItem = copy.deepcopy(itemsForOctaveBalancing[item])
                    newItem['Clk'] = [ itemsForOctaveBalancing[item]['Clk'][1], total ] 
                    newItem['duration'] = [total-itemsForOctaveBalancing[item]['Clk'][1]] 
                    newItem['velocity'] = [0] 
                    self.mel5Data[phraseNum][chId].append ( newItem ) 

                break 
            if ( itemsForOctaveBalancing[item]['Clk'][1] < itemsForOctaveBalancing[item+1]['Clk'][0] ) : 
                newItem = copy.deepcopy(itemsForOctaveBalancing[item])
                newItem['Clk'] = [ itemsForOctaveBalancing[item]['Clk'][1], itemsForOctaveBalancing[item+1]['Clk'][0] ] 
                newItem['duration'] = [itemsForOctaveBalancing[item+1]['Clk'][0] - itemsForOctaveBalancing[item]['Clk'][1] ] 
                newItem['velocity'] = [0] 
                self.mel5Data[phraseNum][chId].append ( newItem ) 
                 

        if ( 0 ) : 
            print ( "DJ Mel 5 Data, Phrase 1" ) 
            for chId in range(len(self.mel5Data[phraseNum] )) :
                print ( "\tChord Id: ", chId ) 
                for item in range(len(self.mel5Data[phraseNum][chId] )) :                 
                    print ( "\t\tNum: ", item, "Data: ", self.mel5Data[phraseNum][chId][item] )                  
                print() 


        #sys.exit(0) 


        return self.mel5Data





        return self.mel5Data

        sys.exit(0) 

        melodyFills = LayerFills.LayerFills(mel5TrainedData, self.wbLevers['tse'], self.wbLevers['phraseLength']) 
        melody = melodyFills.getMeasureAndBeatDataForPhrase ()         


        if ( 1 ) : 
            print() 
            print ( "-------------------------------- DJ MEL Ends --------------------------------------" ) 



        return melody

    def fixOctaves ( self, itemsForOctaveBalancing ) :


        if ( 0 ) : 
            print("\nBefore" )         
            for itemIndex, item in enumerate(itemsForOctaveBalancing) : 
                if ( itemIndex > 0 ) : 
                    print ( itemIndex, "Pitch: ", item['pitches'][0], "diff: " , abs(itemsForOctaveBalancing[itemIndex-1]['pitches'][0] -  itemsForOctaveBalancing[itemIndex]['pitches'][0] ), item['duration'][0], item['Clk'], item['notes'][0] ) 
                else : 
                    print ( itemIndex, "Pitch: ", item['pitches'][0], "diff: " , 0, item['duration'][0], item['Clk'] , item['notes'][0] ) 

        smoothItems = []
        
        fillWithEighthNote = 240
        checkForQuarterNote = 480

        fillWithSixteenthNote = 120
        checkForEighthNote = 240

        if ( random.randint( 0 , 100 ) > 50 ) : 
            fillWithNote = fillWithEighthNote
            checkForNote = checkForQuarterNote
        else :
            fillWithNote = fillWithSixteenthNote
            checkForNote = checkForEighthNote


        if ( 0 ) :
            print ( "FillNote: ", fillWithNote, "check note: ", checkForNote ) 

        numItems = len(itemsForOctaveBalancing) 
        for itemIndex, item in enumerate(itemsForOctaveBalancing) : 
            if ( itemIndex == 0 ) : 
                smoothItems.append( item )
                continue
            diff = abs(itemsForOctaveBalancing[itemIndex-1]['pitches'][0] -  itemsForOctaveBalancing[itemIndex]['pitches'][0] )
            if ( diff > 7 ) : 
                
                newItem = copy.deepcopy ( item )
                if ( itemsForOctaveBalancing[itemIndex-1]['pitches'][0] >  itemsForOctaveBalancing[itemIndex]['pitches'][0] ) :
                    newPitch = newItem['pitches'][0] 
                    chord = itemsForOctaveBalancing[itemIndex]['chord'] 
                    chordTones = MusicTheory.AllChords[chord] 
                    while ( True )  :   # add a chord tone to reduce the big jump 
                        newPitch    +=  1 
                        newPitchStr = MusicTheory.pitchToNotes[ newPitch % 12 ]    
                        if ( newPitchStr in chordTones ) : 
                            newItem['pitches'][0] = newPitch
                            break 
                else : 
                    newPitch  = newItem['pitches'][0] 
                    chord = itemsForOctaveBalancing[itemIndex]['chord'] 
                    chordTones = MusicTheory.AllChords[chord] 
                    while ( True )  :   # add a chord tone to reduce the big jump 
                        newPitch    -= 1 
                        newPitchStr = MusicTheory.pitchToNotes[ newPitch % 12 ]    
                        if ( newPitchStr in chordTones ) : 
                            newItem['pitches'][0] = newPitch
                            break 
                newItem['notes'][0] =  MusicTheory.pitchToNotes[newItem['pitches'][0]%12] 

                cnt = itemIndex 
                itemFound = False
                while ( cnt < numItems ) : 
                    if (  itemsForOctaveBalancing[cnt]['duration'][0] > checkForNote ) : 
                        itemFound = True
                        newItem['Clk'][1] = newItem['Clk'][0] + fillWithNote                  
                        newItem['duration'][0] = newItem['Clk'][1] - newItem['Clk'][0]

                        itemsForOctaveBalancing[cnt]['Clk'][0] += fillWithNote
                        itemsForOctaveBalancing[cnt]['duration'][0] = itemsForOctaveBalancing[cnt]['Clk'][1] - itemsForOctaveBalancing[cnt]['Clk'][0]
                        

                        for i in range ( cnt-1, itemIndex-1, -1 ) : 
                            itemsForOctaveBalancing[i]['Clk'][0] += fillWithNote
                            itemsForOctaveBalancing[i]['Clk'][1] += fillWithNote
                            itemsForOctaveBalancing[i]['duration'][0] = itemsForOctaveBalancing[i]['Clk'][1] - itemsForOctaveBalancing[i]['Clk'][0]
                            
                        break 
                    cnt += 1


                if ( not itemFound ) : 
                    numSmoothItems = len(smoothItems) 
                    cnt = numSmoothItems - 1
                    while ( cnt >= 0 ) : 
                        if ( smoothItems[cnt]['duration'][0] > checkForNote ) : 
                            itemFound = True

                            newItem['Clk'][0] -= fillWithNote 
                            newItem['Clk'][1]  = newItem['Clk'][0] + fillWithNote 
                            newItem['duration'][0] = newItem['Clk'][1] - newItem['Clk'][0]
                        
                            smoothItems[cnt]['Clk'][1] -= fillWithNote
                            smoothItems[cnt]['duration'][0] = smoothItems[cnt]['Clk'][1] - smoothItems[cnt]['Clk'][0]

                            for i in range ( cnt+1, numSmoothItems, 1 ) : 
                                
                                smoothItems[i]['Clk'][0] -= fillWithNote
                                smoothItems[i]['Clk'][1] -= fillWithNote
                                smoothItems[i]['duration'][0] = smoothItems[i]['Clk'][1] - smoothItems[i]['Clk'][0]

                            break 
                        cnt -= 1

                if ( itemFound ) : 
                    smoothItems.append( newItem )                    
                smoothItems.append( item )
            else : 
                smoothItems.append( item )

                

        if ( 0 ) : 
            print("\nAfter" ) 
            for itemIndex, item in enumerate(smoothItems) : 
                if ( itemIndex > 0 ) : 
                    print ( itemIndex, "Pitch: ", item['pitches'][0], "diff: " , abs(smoothItems[itemIndex-1]['pitches'][0] -  smoothItems[itemIndex]['pitches'][0] ), item['duration'][0], item['Clk'] , item['notes'][0] ) 
                else : 
                    print ( itemIndex, "Pitch: ", item['pitches'][0], "diff: " , 0, item['duration'][0], item['Clk'] , item['notes'][0] ) 


        #sys.exit(0) 
        return ( smoothItems ) 
                


    def printLayers ( self ) : 

        print ( "Bass 1: " ) 
        self.bass1Obj.printTrainedData() 

