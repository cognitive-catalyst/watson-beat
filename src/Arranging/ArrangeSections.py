from __future__ import print_function

import random
import collections
import CreateMidiEventsForBass


class ArrangeSections : 

    def __init__ ( self, id, movement, outdir , oneMidiPerLayer) : 
        self.id = id
        self.movement = movement
        self.outdir   = outdir
        self.oneMidiPerLayer = oneMidiPerLayer
        
    def arrange ( self ) : 

        # arranging sections
        if ( 1 ) : 
            print() 
            print ( "ArrangeSections.py" ) 
            sectionsObj = self.movement['SectionsObj'].mood
            print ( "Movement: ", self.id,  "Mood: ", self.movement['mood'], "Complexity: ", self.movement['complexity'],  "Num Uniq Layers:", sectionsObj.numUniqCPs ) 
            print() 
            print ( "Arrangement for Movement" ) 
            for secId in sectionsObj.sections : 
                tse = sectionsObj.sections[secId]['tse'] 
                print ( "\tSection: ", secId, "Uniq Mel Id: ", sectionsObj.sections[secId]['melId'], "Starting MNum: ", sectionsObj.sections[secId]['startMNum'], "Ending MNum: ", sectionsObj.sections[secId]['endMNum'], "TSE: ", tse ) 
                uniqCPId = sectionsObj.sections[secId]['melId'] 
                numChordsInPhrase = sectionsObj.uniqCPSettings[uniqCPId]['numChords']
                phNum = 0
                for chId in sectionsObj.sections[secId]['chords'] : 
                    if ( chId % numChordsInPhrase == 0 ) :
                        print() 
                        print ( "\t\tPhrase: ", phNum + 1, sectionsObj.sections[secId]['phrases'][phNum] ) 
                        phNum += 1
                    print ( "\t\t\tChord: ", chId, sectionsObj.sections[secId]['chords'][chId] ) 
                print() 



        self.midiEventsForSectionLayers = collections.OrderedDict() 
        

        sectionsObj = self.movement['SectionsObj'].mood
        for secId in sectionsObj.sections : 
            

            self.midiEventsForSectionLayers[secId] = collections.OrderedDict() 

            uniqCPId = sectionsObj.sections[secId]['melId'] 
            numChordsInSection = sectionsObj.uniqCPSettings[uniqCPId]['numChords']  
            repCount  = sectionsObj.sections[secId]['repCount']  
            fillsFlag = sectionsObj.sections[secId]['percussionFills'] 


            for chId in sectionsObj.sections[secId]['chords'] : 
                for layer in sectionsObj.sections[secId]['chords'][chId]['layers'] : 

                    if ( layer.endswith('Strings') or layer == 'leftPianoBass' or layer.startswith('rightPiano') or layer.startswith('drums') ) :  # these are phrase level layers. deal with them below
                        continue

                    #if ( not ( layer == 'piano1' or layer == 'bass1' or layer == 'bass2' or layer == 'mel5' or layer == 'rhythmChords' ) ) : 
                    #    continue


                    if ( 0 ) : 
                        print ( "Layer: ", layer ) 

                    if ( layer not in self.midiEventsForSectionLayers[secId] and layer != 'mel5' ) : 
                        self.midiEventsForSectionLayers[secId][layer] = [] 

                    if ( layer == 'mel5' and layer+'Low' not in self.midiEventsForSectionLayers[secId] ) : 
                        self.midiEventsForSectionLayers[secId][layer] = [] 
                        self.midiEventsForSectionLayers[secId][layer+'Low'] = [] 
                        self.midiEventsForSectionLayers[secId][layer+'Med'] = [] 
                        self.midiEventsForSectionLayers[secId][layer+'High'] = [] 


                    actualChordId = chId % numChordsInSection                                    

                    if ( layer == 'bass1' or layer == 'bass2' or layer == 'bass3' ) : 
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEvents ( layer, uniqCPId, secId, chId, sectionsObj.sections[secId]['chords'][chId], self.movement['layers'][uniqCPId][layer][0][actualChordId] ) 
                         
                    if ( 0 and layer == 'bass3' ) : 
                        print ( self.midiEventsForSectionLayers[secId][layer], self.movement['layers'][uniqCPId][layer], uniqCPId, secId, chId, sectionsObj.sections[secId]['chords'][chId], )

                    if ( layer == 'mel5' ) : 
                        low, med, high, all = CreateMidiEventsForBass.CreateMidiEventsForMelody ( layer, uniqCPId, secId, chId, sectionsObj.sections[secId]['chords'][chId], self.movement['layers'][uniqCPId][layer][0][actualChordId] ) 
                        self.midiEventsForSectionLayers[secId][layer] += all
                        self.midiEventsForSectionLayers[secId][layer+'Low'] += low
                        self.midiEventsForSectionLayers[secId][layer+'Med'] += med
                        self.midiEventsForSectionLayers[secId][layer+'High'] += high
                        #self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEvents ( layer, uniqCPId, secId, chId, sectionsObj.sections[secId]['chords'][chId], self.movement['layers'][uniqCPId][layer][0][actualChordId] ) 

                    if ( layer == 'piano1' or layer == 'peruvianRhythmChords') : 
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForPiano ( layer, uniqCPId, secId, chId, repCount, numChordsInSection, sectionsObj.sections[secId]['chords'][chId], self.movement['layers'][uniqCPId][layer][actualChordId] ) 

                    if ( layer == 'rhythmChords'  ) : 
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForRhythmChords ( layer, uniqCPId, secId, chId, repCount, numChordsInSection, sectionsObj.sections[secId]['chords'][chId], self.movement['layers'][uniqCPId][layer][actualChordId] ) 

                    if ( layer == 'brassRhythms' ) : 
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForRhythmChords ( layer, uniqCPId, secId, chId, repCount, numChordsInSection, sectionsObj.sections[secId]['chords'][chId], self.movement['layers'][uniqCPId][layer][0][actualChordId] ) 


            for phId in sectionsObj.sections[secId]['phrases'] :                 

                density = sectionsObj.sections[secId]['phrases'][phId]['density']
                processFillForPhrase = False

                #notation layer
                layerName = "notationLP"
                if ( layerName not in self.midiEventsForSectionLayers[secId] ) : 
                    self.midiEventsForSectionLayers[secId][layerName] = [] 
                layer = 'leftPianoBass'
                self.midiEventsForSectionLayers[secId][layerName] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer] )  
                
                layerName = "notationRP"
                if ( layerName not in self.midiEventsForSectionLayers[secId] ) : 
                    self.midiEventsForSectionLayers[secId][layerName] = [] 
                layer = 'rightPiano'
                lyr = "_rp3"  # pick one of the right piano  layers randomly
                layer1 = layer + lyr                         
                # print ( "SecId: ", secId, "phId: ", phId, "layer: ", layer1 )
                self.midiEventsForSectionLayers[secId][layerName] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer1, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer1])  


                for layer in sectionsObj.sections[secId]['phrases'][phId]['layers'] : 


                    #if ( layer.startswith('drums') ) : 
                    #    continue

                    if ( not ( layer.endswith('Strings') or layer == 'leftPianoBass' or layer.startswith('rightPiano')  or layer.startswith('drums') )  ) :  # these are not phrase level layers. deal with them above
                        continue

                    if ( 0 ) : 
                        print ( layer, "SecId: ", secId, "phId: ", phId ) 
                
                    if ( layer.startswith( 'loStrings' ) ) : 
                        for lyr in [ "_doubleBass", "_cello" ] : 
                            layer1 = layer + lyr 
                            if ( layer1 not in self.midiEventsForSectionLayers[secId] ) : 
                                self.midiEventsForSectionLayers[secId][layer1] = [] 
                            self.midiEventsForSectionLayers[secId][layer1] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer1, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer1] )

                    elif ( layer.startswith( 'midStrings' ) ) : 
                        for lyr in [ "_viola", "_violin2" ] : 
                            layer1 = layer + lyr 
                            if ( layer1 not in self.midiEventsForSectionLayers[secId] ) : 
                                self.midiEventsForSectionLayers[secId][layer1] = [] 
                            self.midiEventsForSectionLayers[secId][layer1] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer1, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer1] )

                    elif ( layer.startswith( 'hiStrings' ) ) : 
                        for lyr in [ "_violin1" ] : 
                            layer1 = layer + lyr 
                            if ( layer1 not in self.midiEventsForSectionLayers[secId] ) : 
                                self.midiEventsForSectionLayers[secId][layer1] = [] 
                            self.midiEventsForSectionLayers[secId][layer1] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer1, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer1] )
                    

                    elif ( layer.startswith( 'arpStrings' ) ) : 
                        lyr = random.choice ( [ "_arp0", "_arp1", "_arp2" ] ) # pick one of the arp layers randomly
                        layer1 = layer + lyr                         
                        if ( layer not in self.midiEventsForSectionLayers[secId] ) : 
                            self.midiEventsForSectionLayers[secId][layer] = [] 
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer1, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer1])  
                        
                    elif ( layer.startswith ( 'drums' ) ) : 
                        if ( layer not in self.midiEventsForSectionLayers[secId] ) : 
                            self.midiEventsForSectionLayers[secId][layer] = []                             
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForPercussions ( layer, density,  uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['percussionFills'], sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer] )  

                        if ( not processFillForPhrase and fillsFlag ) : 
                            layer = 'fillsForDrums'
                            if (  layer not in self.midiEventsForSectionLayers[secId] ) : 
                                self.midiEventsForSectionLayers[secId][layer] = [] 
                            self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForPercussionFills ( layer,  uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['percussionFills'], sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer] )  
                            processFillForPhrase = True
                    
                    elif ( layer.startswith( 'rightPiano' ) ) : 
                        lyr = random.choice ( [ "_rp0", "_rp1", "_rp2" ] ) # pick one of the right piano  layers randomly
                        layer1 = layer + lyr                         
                        #print ( "SecId: ", secId, "phId: ", phId, "layer: ", layer1 )
                        if ( layer not in self.midiEventsForSectionLayers[secId] ) : 
                            self.midiEventsForSectionLayers[secId][layer] = [] 
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer1, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer1])  


                    else : 
                        if ( layer not in self.midiEventsForSectionLayers[secId] ) : 
                            self.midiEventsForSectionLayers[secId][layer] = [] 
                        self.midiEventsForSectionLayers[secId][layer] += CreateMidiEventsForBass.CreateMidiEventsForStrings ( layer, uniqCPId, secId, phId, repCount, numChordsInSection, sectionsObj.sections[secId]['phrases'][phId], self.movement['layers'][uniqCPId][layer] )  


        self.midiEventsForLayers = collections.OrderedDict()
        for secId in self.midiEventsForSectionLayers :
            for layer in self.midiEventsForSectionLayers[secId] : 
                #print("Layer: ",layer,"len: ",len(self.midiEventsForLayers))
                if (self.midiEventsForLayers.get(layer,"0") == "0" ) :
                    #print(layer)
                    self.midiEventsForLayers[layer] = []
 
        for secId in self.midiEventsForSectionLayers : 
            for layer in self.midiEventsForSectionLayers[secId] : 
                self.midiEventsForLayers[layer].extend(self.midiEventsForSectionLayers[secId][layer])
                
                #if ( layer == 'bass1' or layer == 'bass2'  or layer == 'mel5' or layer == 'piano1' or layer == 'rhythmChords' ) : 
                #    CreateMidiEventsForBass.CreateMidiFileForBass ( self.id, secId, layer, self.midiEventsForSectionLayers[secId][layer] ) 
                    
                if ( 0 and layer.startswith('mel5High') ) : 
                    print ( "Section: ", secId, "Layer: ", layer ) 
                    for ev in self.midiEventsForSectionLayers[secId][layer] : 
                        print ( ev ) 
                    print() 
        if self.oneMidiPerLayer:
            for layer in self.midiEventsForLayers :
                CreateMidiEventsForBass.CreateMidiFileForBass ( self.id, 1, layer, self.midiEventsForLayers[layer], self.outdir ) 
        else:
            for secId in self.midiEventsForSectionLayers : 
                for layer in self.midiEventsForSectionLayers[secId] : 

                    CreateMidiEventsForBass.CreateMidiFileForBass ( self.id, secId, layer, self.midiEventsForSectionLayers[secId][layer], self.outdir ) 

                    #if ( layer == 'bass1' or layer == 'bass2'  or layer == 'mel5' or layer == 'piano1' or layer == 'rhythmChords' ) : 
                    #    CreateMidiEventsForBass.CreateMidiFileForBass ( self.id, secId, layer, self.midiEventsForSectionLayers[secId][layer] ) 
                    
                    if ( 0 and layer.startswith('mel5High') ) : 
                        print ( "Section: ", secId, "Layer: ", layer ) 
                        for ev in self.midiEventsForSectionLayers[secId][layer] : 
                            print ( ev ) 
                        print() 


            
