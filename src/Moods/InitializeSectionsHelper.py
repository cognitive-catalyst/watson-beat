from __future__ import print_function
from Skeleton import Constants
from Skeleton import BassRhythms

import sys
import math
import random
import collections


def InitializeSectionsComplex ( self, sections, moodSpecificInfo ) : 
    # get the mood specific info
    fillsFlag = moodSpecificInfo['fills'] 
    if ( 'numChords' in moodSpecificInfo ) :  # this information is passed as parameter to the function  getNumChordsAndDurationForCP ( self, cpId, pl, tse, numChords ) : 
        numChords = moodSpecificInfo['numChords']
    else :
        numChords = -1 

    if 'bassRhythmType' in sections[0] : 
        bassRhythmType = sections[0]['bassRhythmType']
    else :
        bassRhythmType = None 

    if ( 'selectedTempo' in moodSpecificInfo ) : 
        selectedTempo = moodSpecificInfo['selectedTempo'] 
    else : 
        selectedTempo = None 

    idCnt         = 0 
    prevBPM       = 0     
    startMNum     = 1
    uniqIdList    = {}
    totalSeconds  = 0 
    self.sections = collections.OrderedDict () 

    for secId in sections : 

        similarId = sections[secId]['similarId']
        energy = sections[secId]['energy'][0]

        
        if ( 'tse' in sections[secId] ) : 
            tse = sections[secId]['tse']
        else : 
            tse = random.choice ( self.possibleTSEs ) 


        if ( 'bpm' in sections[secId] ) : 
            iniBPM = sections[secId]['bpm']
        else :
            iniBPM = -1

        pl  = self.primaryPL

        # get phrase and measure information
        if ( 'duration' in sections[secId] ) : 

            numSecondsMin = sections[secId]['duration'][0]

            numSecondsMin = int(numSecondsMin) 
            numSecondsMax = int(sections[secId]['duration'][1])

            possibleSecondsForSection = [ i for i in range( numSecondsMin, numSecondsMax+1, 1 ) ] 
            # numSecondsForSection = random.randint ( numSecondsMin, numSecondsMax ) 
                   
            random.shuffle ( possibleSecondsForSection ) 

            if ( iniBPM != -1 ) : 
                possibleBPMs = [ iniBPM - 2, iniBPM - 1, iniBPM, iniBPM + 1, iniBPM + 2 ]  
                random.shuffle ( possibleBPMs ) 
            
            elif ( prevBPM == 0 ) : 
                chosenBPM = random.choice ( self.possibleBPMs ) 
                possibleBPMs = [ chosenBPM - 2, chosenBPM - 1, chosenBPM, chosenBPM + 1, chosenBPM + 2 ]  
                #random.shuffle ( possibleBPMs ) 
                if ( 1 ) : 
                    print ( "Initial chosen BPM: ", chosenBPM ) 
            else : 
                possibleBPMs = [ prevBPM - 2, prevBPM - 1, prevBPM, prevBPM + 1, prevBPM + 2 ]  
                random.shuffle ( possibleBPMs ) 
                if ( 1 ) : 
                    print ( "prev BPM: ", prevBPM ) 

            if ( selectedTempo != None ) : 
                #possibleBPMs = [ selectedTempo - 2, selectedTempo - 1, selectedTempo, selectedTempo + 1, selectedTempo + 2 ]  
                possibleBPMs = [ selectedTempo ]  
                secBPM = selectedTempo

                
            if ( 1 ) : 
                print ( "possible BPMs: ",    possibleBPMs, 'iniBPM: ', iniBPM ) 
                print ( "possible seconds: ", possibleSecondsForSection ) 

            #numSecondsForSection, secBPM = findBestFitForSectionTimeAndBPM ( possibleSecondsForSection, possibleBPMs, tse, pl ) 
            numSecondsForSection, secBPM = findBestFitForSectionTimeGivenBPM ( possibleSecondsForSection, possibleBPMs, tse, pl ) 

            numBeatsPerMeasure = Constants.TSEs[tse]['tsNumerator'] 

            numSecondsPerMeasure = ( numBeatsPerMeasure * 60.0 ) / ( secBPM * 1.0 ) 
            secondsForOnePhrase  = numSecondsPerMeasure * pl                     
            numMeasuresInSection = int(round ( float(numSecondsForSection / numSecondsPerMeasure ), 0 )  )            

        elif ( 'durationInMeasures' in sections[secId] ) : 
            numMeasuresInSection = random.choice ( sections[secId]['durationInMeasures']  )            

            #print ( "Num Measures In Section: ", numMeasuresInSection ) 
            if ( iniBPM != -1 ) : 
                possibleBPMs = [ iniBPM ]  
                random.shuffle ( possibleBPMs ) 
                secBPM = random.choice ( possibleBPMs ) 
            elif ( prevBPM == 0 ) : 
                possibleBPMs = self.possibleBPMs
                secBPM = random.choice ( possibleBPMs ) 
            else : 
                secBPM = prevBPM

            if ( 1 ) : 
                print ( "possible BPMs: ", possibleBPMs, 'iniBPM: ', iniBPM ) 

            if ( selectedTempo != None ) : 
                secBPM = selectedTempo 
                
            numBeatsPerMeasure = Constants.TSEs[tse]['tsNumerator'] 

            numSecondsPerMeasure = ( numBeatsPerMeasure * 60.0 ) / ( secBPM * 1.0 ) 
            secondsForOnePhrase  = numSecondsPerMeasure * pl                     
            numSecondsForSection = numSecondsPerMeasure * numMeasuresInSection


        prevBPM = secBPM
        numPhrases = int ( math.ceil(( float(numSecondsForSection) / float(secondsForOnePhrase) ) ) )

        if ( 1 ) :             
            print ( "SecId: ", secId, "Chosen BPM: ", secBPM, "TSE: ", tse, "numSecondsForSection: ", numSecondsForSection, "numSecondsPerMeasure: ", numSecondsPerMeasure, "numMeasures: ", numMeasuresInSection, "PL: ", pl, "num seconds per phrase: ", secondsForOnePhrase, "num Phrases: ", numPhrases ) 
            print() 

        if ( similarId != -1 and numMeasuresInSection > self.sections[similarId]['numMeasures'] ) :  # if the repeating section is longer, make that the same size as the similar section
            numMeasuresInSection = self.sections[similarId]['numMeasures'] 
            numSecondsForSection = self.sections[similarId]['numSeconds'] 

        totalSeconds += numSecondsForSection        
        numTicks = numMeasuresInSection * Constants.TSEs[tse]['oneMeasure']


        if ( similarId == -1 ) : # unique section not modeled after existing sections            
            self.sections[secId] = { 'id': secId, 'similarId': -1, 'numSeconds': numMeasuresInSection * numSecondsPerMeasure, 'tse': tse, 'bpm': secBPM, 'pl': self.primaryPL, 'key': self.primaryScale, 'numMeasures': numMeasuresInSection, 'repCount': numPhrases, 'totalTicks': numTicks, 'startMNum': startMNum, 'endMNum': startMNum + numMeasuresInSection-1, 'percussionFills': fillsFlag  }
        else : 
            tse    = self.sections[similarId]['tse']
            bpm    = self.sections[similarId]['bpm']
            self.sections[secId] = { 'id': secId,  'similarId': similarId,  'numSeconds':  numSecondsForSection, 'tse': tse, 'bpm': bpm, 'pl': self.primaryPL, 'key': self.primaryScale, 'numMeasures': numMeasuresInSection, 'repCount': numPhrases, 'totalTicks': numTicks, 'startMNum': startMNum, 'endMNum': startMNum + numMeasuresInSection-1, 'percussionFills': fillsFlag  }

        startMNum = startMNum + numMeasuresInSection

        if ( 0 ) : 
            print ( "SecId: ", secId, "Approx Num Seconds For Section: ", numSecondsForSection, "Actual num seconds per section: ", numMeasuresInSection * numSecondsPerMeasure, "Num Measures In Section: ", numMeasuresInSection, "Num Phrases: ", numPhrases  ) 

    #self.maxUniqCPs = 10 
    initialAvailableIds = [ i for i in range(self.minUniqCPs) ] 
    unusedIds = [ i for i in range(self.minUniqCPs, self.maxUniqCPs, 1 ) ] 
    
    self.numUniqCPs = self.minUniqCPs
    TSEsForUniqIds = {} 
    if ( 1 ) : 
        print ( "Min Uniq Ids: ", self.minUniqCPs, "Max Uniq Ids: ", self.maxUniqCPs, "Unused Ids: ", unusedIds ) 

    for secId in self.sections :         
        similarId = sections[secId]['similarId']

        if ( self.sections[secId]['similarId'] != -1 ) : 
            uniqId = self.sections[similarId]['melId']
        else : 
            tse = self.sections[secId]['tse']
            uniqIdForTSE = self.uniqTSEIds[tse]  
            if ( uniqIdForTSE in initialAvailableIds ) : 
                uniqId = self.uniqTSEIds[tse]             
                initialAvailableIds.remove(uniqIdForTSE)
            else : 
                if ( random.randint( 0, 100 ) > 0 and (len(unusedIds) >  0 ) ) : 
                    uniqId = unusedIds[0] 
                    self.numUniqCPs = uniqId+1
                    unusedIds.remove ( uniqId ) 
                else : 
                    uniqId = self.uniqTSEIds[tse]             


        self.sections[secId]['melId'] = uniqId
        TSEsForUniqIds[uniqId] = self.sections[secId]['tse'] 

        if ( 1 ) : 
            print ( "secId: ", secId, "UniqId: ", uniqId, "Unused Ids: ", unusedIds ) 

    if ( 1 ) : 
        print ( "Num Uniq CPs: ", self.numUniqCPs ) 

    self.uniqCPSettings = collections.OrderedDict ()
    for uniqCPId in range( self.numUniqCPs ) : 
        tse = TSEsForUniqIds[uniqCPId] 
        if ( 1 ) : 
            print ( "UniqId: ", uniqCPId, "Tse: ", tse ) 
        #BeatInfo, Patterns, pType = self.setPercussionSettings ( self.primaryTSE )
        BeatInfo, Patterns, pType = self.setPercussionSettings ( tse )



        self.uniqCPSettings[uniqCPId] = { 'scale': self.primaryScale, 'tse': tse, 'pl': self.primaryPL, 'cpSeq': [] , 'numChords': 0 , 'percussionSettings' : { 'BeatInfo': BeatInfo, 'Patterns': Patterns, 'type': pType }  } 

        
        if ( bassRhythmType != None ) : 
            bassRhythmOptions = BassRhythms.CreateBassRhythms ( 'popRhythms', tse ) 
            bassRhythm = collections.OrderedDict() 
            bassRhythm[0] = random.choice ( bassRhythmOptions )  
            bassRhythm[1] = random.choice ( bassRhythmOptions )  
            bassRhythm[2] = random.choice ( bassRhythmOptions )  
            bassRhythm[3] = random.choice ( bassRhythmOptions )  
            bassRhythm[4] = random.choice ( bassRhythmOptions )  
            self.uniqCPSettings[uniqCPId]['bassRhythm'] = bassRhythm 

    if ( 1 ) : 
        for secId in self.sections :         
            print ( "Id", secId, "startMNum: ", self.sections[secId]['startMNum'], "endMNum: ", self.sections[secId]['endMNum'], 'Mel Id: ', self.sections[secId]['melId']  ) 

    # get the number of chords and the duration for each uniq chord progression ( or melID ) 
    for cpId in range(self.numUniqCPs) : 
        self.uniqCPSettings[cpId]['cpSeq'], self.uniqCPSettings[cpId]['numChords']  = getNumChordsAndDurationForCP ( self, cpId, self.primaryPL, self.uniqCPSettings[cpId]['tse'], numChords ) 

    return self

def findBestFitForSectionTimeGivenBPM ( possibleSecondsForSection, possibleBPMs, tse, pl  )  :

    numBeatsPerMeasure = Constants.TSEs[tse]['tsNumerator'] 
    numBeatsInPL = numBeatsPerMeasure * pl * 1.0 

    minDistance = 1000
    chosenDuration = 0
    chosenPhrases = 2
    chosenBPM = 0 

    minMidDistance = 1000
    chosenMidDuration = 0 
    chosenMidPhrases = 2
    chosenMidBPM = 0 

    for bpm in possibleBPMs : 

        secondsForOneBeat = 60.0 / ( bpm * 1.0 ) 

        for numSecondsForSection in possibleSecondsForSection : 

            numBeatsInSection = ( numSecondsForSection * bpm * 1.0 ) / 60.0 
            if ( 0 ) : 
                print ( "Actual Num Phrases: ", round ( numBeatsInSection / numBeatsInPL , 2 ) )
            numPhrasesFloor = int ( math.floor ( numBeatsInSection / numBeatsInPL ) )
            if ( 0 ) :
                print ( "Int Adjusted Num Phrases Floor: ", numPhrasesFloor ) 
            numMeasures = numPhrasesFloor * pl
            actualSecondsFloor = round ( secondsForOneBeat * numBeatsPerMeasure * numMeasures , 2 ) 
            if ( 0 ) :
                print ( "BPM: ", bpm, "Ini Seconds:", numSecondsForSection, "Actual Seconds: ", actualSecondsFloor )         
            diffFloor = abs ( numSecondsForSection - actualSecondsFloor ) 

            numPhrasesCeil = int ( math.ceil ( numBeatsInSection / numBeatsInPL ) )
            if ( 0 ) :
                print ( "Int Adjusted Num Phrases Ceil: ", numPhrasesCeil ) 
            numMeasures = numPhrasesCeil * pl
            actualSecondsCeil = round ( secondsForOneBeat * numBeatsPerMeasure * numMeasures , 2 ) 
            if ( 0 ) :
                print ( "BPM: ", bpm, "Ini Seconds:", numSecondsForSection, "Actual Seconds: ", actualSecondsCeil ) 
            diffCeil = abs ( numSecondsForSection - actualSecondsCeil ) 

            numPhrasesMid = numPhrasesFloor + 0.5 
            if ( 0 ) :
                print ( "Int Adjusted Num Phrases Mid: ", numPhrasesMid ) 
            numMeasures = numPhrasesMid * pl
            actualSecondsMid = round ( secondsForOneBeat * numBeatsPerMeasure * numMeasures , 2 ) 
            if ( 0 ) :
                print ( "BPM: ", bpm, "Ini Seconds:", numSecondsForSection, "Actual Seconds: ", actualSecondsMid ) 
            diffMid = abs ( numSecondsForSection - actualSecondsMid ) 

            if ( minDistance > diffFloor ) : 
                minDistance = diffFloor
                chosenDuration = actualSecondsFloor
                chosenPhrases = numPhrasesFloor
                givenDuration = numSecondsForSection
                chosenBPM = bpm

            if ( minDistance > diffCeil ) : 
                minDistance = diffCeil
                chosenDuration = actualSecondsCeil
                chosenPhrases = numPhrasesCeil
                givenDuration = numSecondsForSection
                chosenBPM = bpm

            if ( minMidDistance > diffMid ) : 
                minMidDistance = diffMid
                chosenMidDuration = actualSecondsMid
                chosenMidPhrases = numPhrasesMid
                givenMidDuration = numSecondsForSection
                chosenMidBPM = bpm            


            if ( 0 ) :
                print() 

    if ( 0 ) :
        print ( "Chosen Phrases: ", chosenPhrases, "num seconds: ", chosenDuration, "given seconds: ", givenDuration ) 
        print ( "Chosen Mid Phrases: ", chosenMidPhrases, "num seconds: ", chosenMidDuration, "given seconds: ", givenMidDuration ) 


    if ( minDistance > minMidDistance ) : 

        if random.randint ( 0, 100 ) > 60 : 
            return chosenDuration, chosenBPM
        else :
            return chosenMidDuration, chosenMidBPM
    
    else : 
        return chosenDuration, chosenBPM



def findBestFitForSectionTimeAndBPM ( possibleSecondsForSection, possibleBPMs, tse, pl  )  :

    numBeatsPerMeasure = Constants.TSEs[tse]['tsNumerator'] 

    while True :
        possibleFullPhraseFits = []  
        possibleHalfPhraseFits = []  
        possibleOneMeasureFits = []

        for numSecondsForSection in possibleSecondsForSection : 
        
            for bpm in possibleBPMs : 
                
                numSecondsPerMeasure    = ( numBeatsPerMeasure * 60.0 ) / ( bpm * 1.0 ) 
                numSecondsForOnePhrase  = numSecondsPerMeasure * pl 
                numSecondsForHalfPhrase = numSecondsForOnePhrase / 2.0

                if ( numSecondsForSection % numSecondsForOnePhrase == 0  ) : 
                    possibleFullPhraseFits.append ( (numSecondsForSection, bpm) )
                elif ( numSecondsForSection % numSecondsForHalfPhrase == 0  ) : 
                    possibleHalfPhraseFits.append ( (numSecondsForSection, bpm) )
                elif ( numSecondsForSection % numSecondsPerMeasure == 0  ) : 
                    possibleOneMeasureFits.append ( (numSecondsForSection, bpm) )
                    
                if ( 0 ) : 
                    print ( "BPM: ", bpm, "Num seconds for section: ", numSecondsForSection, "Num Seconds Per Measure: ", numSecondsPerMeasure, "Num Seconds for One Phrase: ", numSecondsForOnePhrase, "Num Seconds for Half Phrase: ", numSecondsForHalfPhrase ) 

        if ( 0 ) : 
            print()
            print ( "Possibel SecondsForSection: " , possibleSecondsForSection )
            print ( "Possible Full Phrase Fits: ", possibleFullPhraseFits ) 
            print ( "Possible Half Phrase Fits: ", possibleHalfPhraseFits ) 
            print ( "Possible One Measure Fits: ", possibleOneMeasureFits ) 
            
                
        if ( len(possibleFullPhraseFits) == 0 and len(possibleHalfPhraseFits) == 0 and len(possibleOneMeasureFits) == 0 ) : 

            minSeconds = min(possibleSecondsForSection) 
            maxSeconds = max(possibleSecondsForSection) 
            if ( minSeconds-1 > 0 ) : 
                possibleSecondsForSection.append ( minSeconds-0.25 ) 
            possibleSecondsForSection.append ( maxSeconds+0.25 ) 

            minBPM = min(possibleBPMs)
            maxBPM = max(possibleBPMs)
            possibleBPMs.append ( minBPM-1 )
            possibleBPMs.append ( maxBPM+1 )

            if ( 0 )  : 
                print ( "No solution found" )  
                print ( "possibleBPMs : ",  possibleBPMs  ) 
                print ( "possibleSeconds : ",  possibleSecondsForSection  ) 

        else : 
            break 

        
    if ( len(possibleFullPhraseFits) == 0 and len(possibleHalfPhraseFits) == 0 and len(possibleOneMeasureFits) == 0 ) : 
        chosenItem = ( random.choice(possibleSecondsForSection) , random.choice(possibleBPMs ) )

    elif ( len(possibleFullPhraseFits) == 0 and len(possibleHalfPhraseFits) == 0 and len(possibleOneMeasureFits) != 0 ) : 
        chosenItem = random.choice ( possibleOneMeasureFits )

    elif ( len(possibleFullPhraseFits) == 0 and len(possibleHalfPhraseFits) != 0 ) : 
        chosenItem = random.choice ( possibleHalfPhraseFits )

    elif ( len(possibleFullPhraseFits) != 0 ) : 
        chosenItem = random.choice ( possibleFullPhraseFits )
        
    numSecondsForSection = chosenItem[0]
    bpm = chosenItem[1] 
    numSecondsPerMeasure   = ( numBeatsPerMeasure * 60.0 ) / ( bpm * 1.0 ) 
    numSecondsForOnePhrase = numSecondsPerMeasure * pl                     
    numPhrases = int( numSecondsForSection / numSecondsForOnePhrase )                 
    numSecondsForSection = numPhrases * numSecondsForOnePhrase
    numMeasuresInSection = numPhrases * pl    

    if ( 0 ) : 
        print ( "Possible Full Phrase Fits" ) 
        for item in possibleFullPhraseFits: 
            print ( "Num seconds for section: ", item[0], "BPM: ", item[1] ) 
        
                       
        print() 
        print ( "Possible half Phrase Fits" ) 
        for item in possibleHalfPhraseFits: 
            print ( "Num seconds for section: ", item[0], "BPM: ", item[1] ) 
    
    if ( 0 ) :
        print ( "chosenItem: ", chosenItem ) 


    return chosenItem[0], chosenItem[1]

def InitializeSections ( self, sections, moodSpecificInfo ) : 
    
    # get the mood specific info
    fillsFlag = moodSpecificInfo['fills'] 
    if ( 'numChords' in moodSpecificInfo ) :  # this information is passed as parameter to the function  getNumChordsAndDurationForCP ( self, cpId, pl, tse, numChords ) : 
        numChords = moodSpecificInfo['numChords']
    else :
        numChords = -1 

    # calculate number of measures per section 
    totalBeats = ( self.primaryBPM * self.durationInSecs ) // 60
    numBeatsPerMeasure = Constants.TSEs[self.primaryTSE]['tsNumerator']
    totalMeasures = totalBeats // numBeatsPerMeasure 
    
    #num seconds per beat
    numSecondsPerBeatFlt = round ( ( 60.0 / self.primaryBPM ) , 2 )
    
    #num seconds per measure 
    numSecondsPerMeasure = numSecondsPerBeatFlt *  numBeatsPerMeasure 

    if ( 1 ) : 
        print ( "Duration in Seconds: ", self.durationInSecs ) 
        print ( "Total Beats: ", totalBeats ) 
        print ( "Total Measures: ", totalMeasures ) 
        print ( "Num Seconds Per Measure: ", numSecondsPerMeasure ) 
        print ( "Uniq CP Ids: ", self.numUniqCPs ) 
        print()

    self.sections = collections.OrderedDict () 
    totalSeconds = 0
    startMNum = 1
    uniqIdList = {}
    idCnt = 0 

    tonyawards = True
    tonyawards = False
    uniqIdCnt = 0 

    for secId in sections : 

        similarId = sections[secId]['similarId']
        
        energy = sections[secId]['energy'][0]

        if ( energy == 'demo' ) : 
            numPhrases = 2            
            numMeasuresInSection = self.primaryPL * 2
            numSecondsForSection = numSecondsPerMeasure * numMeasuresInSection
            sections[secId]['duration'][0] = numSecondsForSection
            sections[secId]['duration'][1] = numSecondsForSection
            if ( 1 ) :
                print ( "max and min duration:", sections[secId]['duration'][0] , sections[secId]['duration'][1] )             

        # get phrase and measure information
        if ( 'duration' in sections[secId] ) : 
                
            numSecondsMin = sections[secId]['duration'][0]
            if ( numSecondsMin != 'rest' ) : 
                numSecondsMin = int(numSecondsMin) 
                numSecondsMax = int(sections[secId]['duration'][1])
                numSecondsForSection = random.randint ( numSecondsMin, numSecondsMax ) 
            else : 
                if ( totalSeconds + 4 > self.durationInSecs ) :
                    numSecondsForSection = 4 
                else : 
                    numSecondsForSection = self.durationInSecs - totalSeconds 


            totalSeconds += numSecondsForSection
            numMeasuresInSection = int(round ( float(numSecondsForSection / numSecondsPerMeasure ), 0 )  )

        elif ( 'durationInMeasures' in sections[secId] ) : 
            numMeasuresInSection = random.choice ( sections[secId]['durationInMeasures']  )            
            #print ( "Num Measures In Section: ", numMeasuresInSection ) 


            
        if ( similarId != -1 and numMeasuresInSection > self.sections[similarId]['numMeasures'] ) :  # if the repeating section is longer, make that the same size as the similar section
            numMeasuresInSection = self.sections[similarId]['numMeasures'] 

        numPhrases = math.ceil ( float ( numMeasuresInSection*1.0 / self.primaryPL*1.0 ) ) 
        numTicks = numMeasuresInSection * Constants.TSEs[self.primaryTSE]['oneMeasure']
        uniqId = random.randint ( 0, self.numUniqCPs-1 )                        

        if ( tonyawards ) : 
            uniqId = uniqIdCnt
            uniqIdCnt += 1

        if ( uniqId not in uniqIdList ) : 
            uniqIdList[uniqId] = idCnt 
            uniqId = idCnt
            idCnt += 1
        else : 
            uniqId = uniqIdList[uniqId] 
            
        if ( similarId  == -1 ) : # unique section not modeled after existing sections            
            self.sections[secId] = { 'id': secId, 'similarId': -1, 'totalSeconds': numMeasuresInSection * numSecondsPerMeasure, 'tse': self.primaryTSE, 'bpm': self.primaryBPM, 'pl': self.primaryPL, 'key': self.primaryScale, 'numMeasures': numMeasuresInSection, 'repCount': numPhrases, 'totalTicks': numTicks, 'startMNum': startMNum, 'endMNum': startMNum + numMeasuresInSection-1, 'melId': uniqId, 'percussionFills': fillsFlag  }
        else : 
            uniqId = self.sections[similarId]['melId']
            self.sections[secId] = { 'id': secId,  'similarId': similarId,  'totalSeconds': numMeasuresInSection * numSecondsPerMeasure, 'tse': self.primaryTSE, 'bpm': self.primaryBPM, 'pl': self.primaryPL, 'key': self.primaryScale, 'numMeasures': numMeasuresInSection, 'repCount': numPhrases, 'totalTicks': numTicks, 'startMNum': startMNum, 'endMNum': startMNum + numMeasuresInSection-1, 'melId': uniqId, 'percussionFills': fillsFlag  }

        startMNum = startMNum + numMeasuresInSection

        if ( 0 ) : 
            print ( "SecId: ", secId, "Approx Num Seconds For Section: ", numSecondsForSection, "Actual num seconds per section: ", numMeasuresInSection * numSecondsPerMeasure, "Num Measures In Section: ", numMeasuresInSection, "Num Phrases: ", numPhrases  ) 

    self.numUniqCPs = idCnt 
    self.uniqCPSettings = collections.OrderedDict ()
    for uniqCPId in range( self.numUniqCPs ) : 
        BeatInfo, Patterns, pType = self.setPercussionSettings ( self.primaryTSE )
        self.uniqCPSettings[uniqCPId] = { 'scale': self.primaryScale, 'bpm': self.primaryBPM, 'tse': self.primaryTSE, 'pl': self.primaryPL, 'cpSeq': [] , 'numChords': 0 , 'percussionSettings' : { 'BeatInfo': BeatInfo, 'Patterns': Patterns, 'type': pType }  } 

    if ( 1 ) : 
        for secId in self.sections :         
            print ( "Id", secId, "startMNum: ", self.sections[secId]['startMNum'], "endMNum: ", self.sections[secId]['endMNum'], 'Mel Id: ', self.sections[secId]['melId']  ) 

    # get the number of chords and the duration for each uniq chord progression ( or melID ) 
    for cpId in range(self.numUniqCPs) : 
        self.uniqCPSettings[cpId]['cpSeq'], self.uniqCPSettings[cpId]['numChords']  = getNumChordsAndDurationForCP ( self, cpId, self.primaryPL, self.primaryTSE, numChords ) 


    #sys.exit(0) 
    return self


def getNumChordsAndDurationForCP ( self, cpId, pl, tse, numChords ) : 

    #fiveMeasureTicks    =  Constants.TSEs[tse]['oneMeasure'] * 5
    #fourMeasureTicks    =  Constants.TSEs[tse]['oneMeasure'] * 4 
    #threeMeasureTicks   =  Constants.TSEs[tse]['oneMeasure'] * 3 
    #quarterMeasureTicks =  Constants.TSEs[tse]['oneMeasure'] / 4 
    
    print ( "NumChords: ", numChords ) 

    halfMeasureTicks    =  random.choice(Constants.TSEs[tse]['halfMeasure'] ) 
    fullMeasureTicks    =  Constants.TSEs[tse]['oneMeasure'] 
    twoMeasureTicks     =  Constants.TSEs[tse]['oneMeasure'] * 2 
    oneHalfMeasureTicks =  halfMeasureTicks * 3 
    maxduration         =  Constants.TSEs[tse]['oneMeasure'] * pl 


    if ( pl == 2 ) : 
        numChords = random.choice ( [ 1, 2, 2 ] ) 


    if ( numChords == -1 ) :  # if mood specific info does not include number of chords, then determine number of chords here
        if ( pl == 2 ) : 
            numChords = random.choice ( [ 1, 2, 2 ] ) 
            cpDurationOptions   = [ halfMeasureTicks, fullMeasureTicks, twoMeasureTicks ]
        else : 
            numChords = random.choice ( [ 1, 2, 3, 4 ] ) 
            cpDurationOptions   = [ halfMeasureTicks, fullMeasureTicks, oneHalfMeasureTicks, twoMeasureTicks ]
    else : # mood specific info has passed information on number of chords 
        cpDurationOptions   = [  fullMeasureTicks, oneHalfMeasureTicks, twoMeasureTicks ]
    
    tryNum = 1
    if ( numChords == 1 ) : 
        ChordDurations = [ maxduration ]         
        if ( 1 ) : 
            print ( "Chord Progression Sequence found in try number: ", tryNum, " Sequence : ", ChordDurations  ) 
        return ChordDurations, numChords
        
    print ( "NumChords: ", numChords ) 

    while True :                 
        currTicks = 0 
        cpDurationSeq = []
        chordInfo = {}
        
        for i in range (  numChords ) : 
                
            cpDuration = random.choice ( cpDurationOptions ) 
            currTicks += cpDuration
            cpDurationSeq.append ( cpDuration ) 
            
            if ( currTicks > maxduration ) : 
                break 
                
        if ( currTicks == maxduration ) : 
            break 

        if ( 0 ) :
            print ( "Try Number: ", tryNum, " Sequence not found: ",  "Num Chords: ", numChords, "Sequence: ", cpDurationSeq, "Max Duration: ", maxduration, "curr ticks: ", currTicks ) 

        tryNum += 1

    ChordDurations = cpDurationSeq
    if ( 1 ) : 
        print ( "Chord Progression Sequence found in try number: ", tryNum, " Sequence : ", ChordDurations  ) 

        
    return ChordDurations, numChords

