from __future__ import print_function

import sys
import random
import collections


def InitializeChordsAndPhraseForSections ( self, sections ) :

    # set the number of layers in section based on energy levels
    globalTick = 0 
    allLayers = self.layers.keys() 
    for secId in sections : 
        energy = random.choice ( sections[secId]['energy'] ) 
        direction = random.choice ( sections[secId]['direction'] ) 
        slope = random.choice ( sections[secId]['slope'] ) 
        uniqCPId = self.sections[secId]['melId'] 

        mustHaveLayers = []
        mustNotHaveLayers = [] 
        mustOnlyHaveLayers = []
        mustOnlyHaveFlag = False

        if ( 'mustOnlyHaveGroups' in sections[secId] ) : 
            
            for groupLyrId in sections[secId]['mustOnlyHaveGroups'] :   # groupLyrId = rhythm, melody etc
                groupDensity = sections[secId]['mustOnlyHaveGroups'][groupLyrId]  # groupdensity = heavy, medium or lite
                numLayersInGroup = self.groupLayers[groupLyrId][groupDensity] 
                for i in range ( numLayersInGroup ) : 
                    layer = random.choice ( self.groupLayers[groupLyrId]['layers'] ) 
                    while layer in mustOnlyHaveLayers : 
                        layer = random.choice ( self.groupLayers[groupLyrId]['layers'] ) 
                    mustOnlyHaveLayers.append(layer)                
            mustOnlyHaveFlag = True

        if ( 'mustOnlyHaveLayers' in sections[secId] ) : 
            for layer in sections[secId]['mustOnlyHaveLayers'] : 
                if ( layer == 'melody' ) : 
                    layer = 'mel5'
                mustOnlyHaveLayers.append(layer)
            mustOnlyHaveFlag = True

        if (not mustOnlyHaveFlag and 'mustHaveGroups' in sections[secId] ) :             
            for groupLyrId in sections[secId]['mustHaveGroups'] :   # groupLyrId = rhythm, melody etc
                groupDensity = sections[secId]['mustHaveGroups'][groupLyrId]  # groupdensity = heavy, medium or lite
                numLayersInGroup = self.groupLayers[groupLyrId][groupDensity] 
                for i in range ( numLayersInGroup ) : 
                    layer = random.choice ( self.groupLayers[groupLyrId]['layers'] ) 
                    while layer in mustHaveLayers : 
                        layer = random.choice ( self.groupLayers[groupLyrId]['layers'] ) 
                    #mustHaveLayers[layer] = True 
                    mustHaveLayers.append(layer)
                                
        if ( not mustOnlyHaveFlag and  'mustHaveLayers' in sections[secId] ) : 
            for layer in sections[secId]['mustHaveLayers'] :  
                if ( layer == 'melody' ) : 
                    layer = 'mel5'
                mustHaveLayers.append(layer)
                #mustHaveLayers[layer] = True 

        if ( not mustOnlyHaveFlag and 'mustNotHaveGroups' in sections[secId] ) : 
            for groupLyrId in sections[secId]['mustNotHaveGroups'] : 
                for layer in self.groupLayers[groupLyrId]['layers'] : 
                    #mustNotHaveLayers[layer] = True 
                    mustNotHaveLayers.append(layer)

        if ( not mustOnlyHaveFlag and 'mustNotHaveLayers' in sections[secId] ) : 
            for layer in sections[secId]['mustNotHaveLayers'] :                 
                if ( layer == 'melody' ) : 
                    layer = 'mel5'
                #mustNotHaveLayers[layer] = True 
                mustNotHaveLayers.append(layer)

        if ( mustOnlyHaveFlag ) : 
            mustHaveLayers = mustOnlyHaveLayers
            mustNotHaveLayers = list( set(allLayers) - set(mustHaveLayers) ) 

        if ( 1 ) : 
            print () 
            print ( "Section settings: Id: " , secId, "Energy: ", energy, "Direction: ", direction, "Slope: ", slope ) 
            if mustHaveLayers != None :
                for layer in mustHaveLayers : 
                    print ( "Must Have layer: ", layer )
                print() 
            if mustNotHaveLayers != None :
                for layer in mustNotHaveLayers : 
                    print ( "Must Not Have layer: ", layer )
                print() 

        self.sections[secId]['chords'], self.sections[secId]['phrases'], globalTick = getChordSettingsForSection ( self, secId, energy, direction, slope, uniqCPId, globalTick, mustHaveLayers, mustNotHaveLayers ) 

        if ( 1 ) :
            print() 
            print ("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "End Section: ",  secId,   "   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" ) 


    return self

def getChordSettingsForSection ( self, secId, energy, direction, slope, uniqCPId, globalTick, mustHaveLayers, mustNotHaveLayers ) : 

    phrases = collections.OrderedDict()  
    chords  = collections.OrderedDict() 
    phId = 0  # curr phrase num
    chId = 0  # curr chord  num
    phLayers = [] 
    currTick   = 0 
    totalTicks = self.sections[secId]['totalTicks'] 
    uniqId     = self.sections[secId]['melId'] 
    chordSeq   = self.uniqCPSettings[uniqCPId]['cpSeq'] 
    numChordsInPhrase = self.uniqCPSettings[uniqCPId]['numChords'] 

    startMNum = self.sections[secId]['startMNum'] 
    pl = self.sections[secId]['pl'] 

    if ( energy == 'demo' ) : 
        currNumLayers = 3 
        maxLayers = 3
        minLayers = 2
    else: 

        currNumLayers = random.randint ( self.MaxAndMinLayersForEnergy[energy]['initialMin'], self.MaxAndMinLayersForEnergy[energy]['initialMax'] )  
        maxLayers = self.MaxAndMinLayersForEnergy[energy]['max']
        minLayers = self.MaxAndMinLayersForEnergy[energy]['min']

    if ( 1 ) : 
        print ( "Current number of layers: ", currNumLayers, "max layers: ", maxLayers, "min Layers: ", minLayers )  

    if ( slope == 'gradual' ) : 
        multiplier = random.choice ( [1, 2, 1] ) 
    elif ( slope == 'steep' ) : 
        multiplier = random.choice ( [2, 2, 1] ) 
    else : 
        multiplier = random.choice ( [0, 1, 1] ) 
        
    if ( direction == 'up' ) : 
        addLayers = 1
    else : 
        addLayers = -1

    adder = multiplier * addLayers
        
    actualNumSecondsInSection = self.sections[secId]['numSeconds'] 
    numPhrasesInSection       = self.sections[secId]['repCount'] 
    approxNumChordsInSection  = numPhrasesInSection * len(chordSeq) # why approximate, because the last phrase may not be a complete phrase 

    if ( actualNumSecondsInSection <= 4 ) : 
        freqOfLayerChanges = approxNumChordsInSection 
        chordBased = True 
    else : 
        freqOfLayerChanges = numPhrasesInSection 
        chordBased = False

    if ( 1 ) :
        print() 
        print ("Initial." , "Section id: ", secId, "Energy: ", energy, "Direction: ", direction, "slope: ", slope, "Slope Multiplier: ", multiplier, "AddLayers: ", addLayers, "Final Adder: ", adder, "curr density: ", currNumLayers  ) 
    

    density = 0 
    layers = [] 
    layers, density = getLayersBasedOnEnergy ( self, energy, currNumLayers, layers, mustHaveLayers, mustNotHaveLayers )  
    phLayers += layers # has all the phrase layers

    similarId = self.sections[secId]['similarId']
    

    if ( 0 ) : 
        print ( "Chord Seq: ", chordSeq ) 

    while ( currTick < totalTicks ) : 

        for chordTick in chordSeq : 

            if  ( 0 ) : 
                print ( "Sec Id: ", secId, "chordTick: ", chordTick, "currtick: ", currTick, "totalTicks: ", totalTicks, "phraseId: ", phId, "chId: ", chId, "numChordsInPhrase: ", numChordsInPhrase    ) 


            if ( currTick >= totalTicks ) : 
                firstChordInPhrase = numChordsInPhrase * ( phId) 
                if ( 0 ) : 
                    print ( "I am here 1" ) 
                    print ( "chId: ", chId, "phId: ", phId, "firtsChordInPhrase: ", firstChordInPhrase, "num chords: " , numChordsInPhrase ) 

                if ( similarId != -1 ) : 
                    phLayers = self.sections[similarId]['phrases'][phId]['layers'] 

                phrases[phId] = { 'layers': list(set(phLayers)), 'globalEndTick': chords[chId-1]['globalEndTick'], 'globalStartTick': chords[firstChordInPhrase]['globalStartTick'],  'startMNum': startMNum, 'endMNum': startMNum + pl-2 , 'density': density } 
                phLayers = [] 
                phId += 1
                startMNum += pl 
                break 

            if ( chordTick + currTick <= totalTicks ) :

                if ( similarId != -1 ) : 
                    layers = self.sections[similarId]['chords'][chId]['layers'] 

                chords[chId] = { 'startTick': currTick, 'endTick': chordTick + currTick, 'layers': layers, 'duration': chordTick, 'density': density, 'globalStartTick': currTick + globalTick, 'globalEndTick': chordTick + currTick + globalTick }
                currTick += chordTick
                chId += 1
                firstChordInPhrase = numChordsInPhrase * ( phId) 
                if ( 0 ) : 
                    print ( "I am here 2" ) 
                    print ( "chId: ", chId, "phId: ", phId, "firtsChordInPhrase: ", firstChordInPhrase, "num chords: " , numChordsInPhrase ) 

                if ( chId % numChordsInPhrase == 0 ) : # account for the layers for the phrase

                    if ( similarId != -1 ) : 
                        phLayers = self.sections[similarId]['phrases'][phId]['layers'] 

                    phrases[phId] = { 'layers': list(set(phLayers)), 'globalEndTick': chords[chId-1]['globalEndTick'], 'globalStartTick': chords[firstChordInPhrase]['globalStartTick'] ,  'startMNum': startMNum, 'endMNum': startMNum + pl-1  , 'density': density } 
                    phLayers = [] 
                    phId += 1
                    startMNum += pl 

            else :

                diff = totalTicks - currTick

                if ( similarId != -1 ) : 
                    layers = self.sections[similarId]['chords'][chId]['layers'] 

                chords[chId] = { 'startTick': currTick, 'endTick': diff + currTick, 'layers': layers, 'duration': diff, 'density': density, 'globalStartTick': currTick + globalTick, 'globalEndTick': diff + currTick + globalTick,  }
                currTick += diff 
                chId += 1                    
                firstChordInPhrase = numChordsInPhrase * ( phId) 
                if ( 0 ) : 
                    print ( "I am here 3" ) 
                    print ( "chId: ", chId, "phId: ", phId, "firtsChordInPhrase: ", firstChordInPhrase, "num chords: " , numChordsInPhrase ) 

                if ( similarId != -1 ) : 
                    phLayers = self.sections[similarId]['phrases'][phId]['layers'] 

                phrases[phId] = { 'layers': list(set(phLayers)), 'globalEndTick': chords[chId-1]['globalEndTick'], 'globalStartTick': chords[firstChordInPhrase]['globalStartTick'], 'startMNum': startMNum, 'endMNum': startMNum + pl-1 , 'density': density  } 
                phLayers = [] 
                phId += 1
                startMNum += pl 
                break 
            
            # chord based layer change 
            if ( chordBased ) : 
                currNumLayers += adder
                if ( currNumLayers < minLayers ) : 
                    currNumLayers = minLayers
                elif ( currNumLayers > maxLayers ) : 
                    currNumLayers = maxLayers
                if ( 0 ) : 
                    print ("Next Chord." , "Section id: ", secId, "Energy: ", energy, "Direction: ", direction, "slope: ", slope, "Slope Multiplier: ", multiplier, "AddLayers: ", addLayers, "Final Adder: ", adder, "curr density: ", currNumLayers  ) 

                layers, density = getLayersBasedOnEnergy ( self, energy, currNumLayers, layers, mustHaveLayers, mustNotHaveLayers ) 
                phLayers += layers # contains all the layers for the phrase

        # phrase based layer change 
        currNumLayers += adder
        if ( currNumLayers < minLayers ) : 
            currNumLayers = minLayers
        elif ( currNumLayers > maxLayers ) : 
            currNumLayers = maxLayers
        layers, density = getLayersBasedOnEnergy ( self, energy, currNumLayers, layers, mustHaveLayers, mustNotHaveLayers ) 
        if ( 0 ) : 
            print ("Next Phrase." , "Section id: ", secId, "Energy: ", energy, "Direction: ", direction, "slope: ", slope, "Slope Multiplier: ", multiplier, "AddLayers: ", addLayers, "Final Adder: ", adder, "curr density: ", currNumLayers  ) 

        phLayers += layers   # contains all the layers for the phrase

    globalTick = chords[chId-1]['globalEndTick'] 

    return chords, phrases, globalTick



def getLayersBasedOnEnergy ( self, energy, numLayers, prevLayers, mustHaveLayers, mustNotHaveLayers ) :

    
    if ( 'drumsCymbalSwell' in prevLayers ) : 
        noCymbalSwell = True 
    else :
        noCymbalSwell = False

    if ( 1 ) : 
        print ( "Energy: ", energy, "Num Layers: ", numLayers ) 

    layers = []
    density = 0 

    if ( energy == 'demo' and  len(prevLayers) == 0 ) : 
        layers = [ 'bass2', 'mel5' ] 
        return layers, 2
    elif ( energy == 'demo' and  len(prevLayers) > 0 ) : 
        layers = [ 'bass2', 'mel5' ]  + self.percussionDesc
        return layers, len(layers)



    layers = list(set(mustHaveLayers)) 
    density = len(layers) 

    layers = list(set(layers) - set(mustNotHaveLayers)) 
    density = len(layers) 


    if ( len(prevLayers) == 0 or len(prevLayers) <= numLayers ) : # first phrase in section (so empty prevlayer) or go up in density or have the same density

        searchLayers = self.layers.keys() 
        searchLayers = list(set(searchLayers) - set(mustNotHaveLayers))  # remove the mustNotHaveLayers
        cnt = 0

        if ( len(prevLayers) <=  numLayers ) : # go up in density or have the same density 
            layers += prevLayers
            layers = list(set(layers)) 
            density = len(layers) 


        while ( density < numLayers and cnt < 100 ) : 
            cnt += 1
            lyr = random.choice ( searchLayers ) 
            if ( lyr not in layers ) : 
                layers.append ( lyr ) 
                density += 1

    elif ( len(prevLayers) > numLayers ) : # go down in density 
        searchLayers = prevLayers 
        searchLayers = list(set(searchLayers) - set(mustNotHaveLayers))  # remove the mustNotHaveLayers
        cnt = 0 
        while ( density < numLayers and cnt < 100 ) : 
            cnt += 1
            lyr = random.choice ( searchLayers ) 
            if ( lyr not in layers ) : 
                layers.append ( lyr ) 
                density += 1
                

    if ( 1 ) : 
        print() 
        print ( "Previous Layers: ", prevLayers , "prev Density: ", len(prevLayers) ) 
        print ( "Current  Layers: ", layers , "current Density: ", density ) 
    

    return layers, density


