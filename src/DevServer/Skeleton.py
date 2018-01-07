from __future__ import print_function

from Elements.Inspire  import * 
from Elements.Epic  import * 
from Elements.CalmWaters  import * 
from Elements.ChoppyWaters  import * 
from Genre.Genre import *
from Genre.ClassicalGenre import *
from Genre.GeneralGenre import *
from Arranging.ArrangeSections import *
from MoodGenreTemplates.Template import * 

from Moods.Mood import Mood



import re
import os
import sys
import json
import random
import Section
import Elements.Water
import Elements.Elements
import HelperFunctions
import CreateMidiFiles
import DevServer.Server

class Template : 



    def __init__ ( self, iniFname, tempo ) : 
 
        self.tempo = tempo           
        self.ReadIniFile ( iniFname ) 

    def ReadIniFile ( self, fname ) : 

        fin = open(fname) 
        lines = [line.rstrip('\n') for line in open(fname)]        
        fin.close()

        self.movements = collections.OrderedDict() 

        for line in lines : 

            splitLine = re.split (r'[\s*,=]', line ) 

            if ( line.startswith ('numMovements') ) : 
                self.numMovements = int(splitLine[1])
                if ( 1 ) : 
                    print ( "Num Movements: ", self.numMovements ) 

            if ( line.startswith ('movementId') ) : 
                mvmtId = int(splitLine[1])
                self.movements[mvmtId] = collections.OrderedDict()
                sections = collections.OrderedDict() 
                self.movements[mvmtId]['uniqTSEs'] = {} 
                self.movements[mvmtId]['duration'] = 0
                uniqId = 0

            if ( line.startswith ('movementDuration') ) : 
                mvmtDuration = int(splitLine[1])
                self.movements[mvmtId]['duration'] = mvmtDuration

            if ( line.startswith ('mood') ) : 
                mood = splitLine[1]
                self.movements[mvmtId]['mood'] = mood

            if ( line.startswith ('rhythmSpeed') ) : 
                rhythmSpeed = splitLine[1]
                self.movements[mvmtId]['rhythmSpeed'] = rhythmSpeed 

            if ( line.startswith ('complexity') ) : 
                complexity = splitLine[1]
                self.movements[mvmtId]['complexity'] = complexity


            if ( line.startswith ('#end movement') ) : 
                if ( len(self.movements[mvmtId]['uniqTSEs']) == 0 ) : 
                    self.movements[mvmtId]['uniqTSEs']['4/4'] = 0
                self.movements[mvmtId]['sectionSettings'] = sections

            if ( line.startswith ('section') ) : 
                newSplit = re.split (r'[:,\']', line ) 
                cnt = 0 
                
                while ( cnt < (len(newSplit)) )  : 

                    newSplit[cnt] = newSplit[cnt].strip() # remove leading and trailing white space

                    if ( newSplit[cnt] == 'id' ) : 
                        cnt += 1
                        id = int(newSplit[cnt]) 
                        sections[id] = collections.OrderedDict() 
                        sections[id]['similarId'] = -1  # initially set similar id to -1
                        sections[id]['tse'] = '4/4'  # set this as default

                    elif ( newSplit[cnt] == 'similarTo' ) : 
                        cnt += 1
                        similarId = int(newSplit[cnt]) 
                        if ( similarId >= id ) :  # similar id doesnt exist yet. so ignore
                            continue                         
                        else : 
                            sections[id]['energy'] = sections[similarId]['energy']
                            sections[id]['slope'] = sections[similarId]['slope']
                            sections[id]['direction'] = sections[similarId]['direction']
                            sections[id]['similarId'] = similarId 


                    elif ( newSplit[cnt] == 'tse' ) : 
                        cnt += 2
                        tse = newSplit[cnt]
                        print ( "TSE: ", tse ) 
                        sections[id]['tse'] = tse
                        if ( tse not in self.movements[mvmtId]['uniqTSEs'] ) :                        
                            self.movements[mvmtId]['uniqTSEs'][tse] = uniqId 
                            uniqId += 1

                    elif ( newSplit[cnt] == 'bpm' ) : 
                        cnt += 1                        
                        bpm = int(newSplit[cnt])
                        print ( "BPM: ", bpm ) 
                        sections[id]['bpm'] = bpm


                    elif ( newSplit[cnt] == 'energy' ) : 
                        cnt += 2
                        energy = newSplit[cnt]
                        energy = energy.replace('or', "" ).split()
                        #print ( "Energy: ", energy ) 
                        sections[id]['energy'] = energy

                    elif ( newSplit[cnt] == 'duration' ) : 
                        cnt += 2
                        duration = newSplit[cnt]
                        duration = duration.replace('to', "" )
                        duration = duration.replace('seconds', "" ).split()
                        #print ( "Duration: ", duration ) 
                        sections[id]['duration'] = duration

                    elif ( newSplit[cnt] == 'durationInMeasures' ) : 
                        cnt += 2
                        duration = newSplit[cnt]
                        duration = duration.replace('or', "" )
                        duration = duration.split()
                        duration = [ int(i) for i in duration ] 
                        sections[id]['durationInMeasures'] = duration
                        print ( "Duration Choices In Measures: ", duration ) 

                    elif ( newSplit[cnt] == 'slope' ) : 
                        cnt += 2
                        slope = newSplit[cnt]
                        slope = slope.replace('or', "" ).split()
                        #print ( "Slope: ", slope ) 
                        sections[id]['slope'] = slope

                    elif ( newSplit[cnt] == 'direction' ) : 
                        cnt += 2
                        direction = newSplit[cnt]
                        direction = direction.replace('or', "" ).split()
                        #print ( "Direction: ", direction ) 
                        sections[id]['direction'] = direction


                    elif ( newSplit[cnt].startswith ('mustHaveGroup') ) : 
                        cnt += 2
                        mustHave = newSplit[cnt]                        
                        layerDetails = mustHave.split()
                        #print ( "layerDetails: ", layerDetails ) 
                        if ( len(layerDetails) == 1 ) : 
                            layerDetails.append( 'medium' )

                        if ( 'mustHaveGroups' not in sections[id] ) : 
                            sections[id]['mustHaveGroups'] = collections.OrderedDict () 
                        sections[id]['mustHaveGroups'][layerDetails[0]] = layerDetails[1]
                        #print ( "mustHave Group: ", layerDetails ) 

                    elif ( newSplit[cnt].startswith ('mustOnlyHaveGroup') ) : 
                        cnt += 2
                        mustHave = newSplit[cnt]                        
                        layerDetails = mustHave.split()
                        #print ( "layerDetails: ", layerDetails ) 
                        if ( len(layerDetails) == 1 ) : 
                            layerDetails.append( 'medium' )

                        if ( 'mustOnlyHaveGroups' not in sections[id] ) : 
                            sections[id]['mustOnlyHaveGroups'] = collections.OrderedDict () 
                        sections[id]['mustOnlyHaveGroups'][layerDetails[0]] = layerDetails[1]
                        #print ( "mustHave Group: ", layerDetails ) 

                    elif ( newSplit[cnt].startswith ('mustHaveLayer') ) : 
                        cnt += 2
                        mustHave = newSplit[cnt]                        
                        if ( 'mustHaveLayers' not in sections[id] ) : 
                            sections[id]['mustHaveLayers'] = collections.OrderedDict () 
                        sections[id]['mustHaveLayers'][mustHave] = True
                        #print ( "mustHave Layer: ", sections[id]['mustHaveLayers'] ) 

                    elif ( newSplit[cnt].startswith ('mustOnlyHaveLayer') ) : 
                        cnt += 2
                        mustHave = newSplit[cnt]                        
                        if ( 'mustOnlyHaveLayers' not in sections[id] ) : 
                            sections[id]['mustOnlyHaveLayers'] = collections.OrderedDict () 
                        sections[id]['mustOnlyHaveLayers'][mustHave] = True
                        #print ( "mustHave Layer: ", sections[id]['mustHaveLayers'] ) 


                    elif ( newSplit[cnt].startswith ('mustNotHaveGroup') ) : 
                        cnt += 2
                        mustNotHave = newSplit[cnt]                        

                        if ( 'mustNotHaveGroups' not in sections[id] ) : 
                            sections[id]['mustNotHaveGroups'] = collections.OrderedDict () 
                        sections[id]['mustNotHaveGroups'][mustNotHave] = True 
                        #print ( "mustNot Have Group: ", sections[id]['mustNotHaveGroups'] ) 

                    elif ( newSplit[cnt].startswith ('mustNotHaveLayer') ) : 
                        cnt += 2
                        mustNotHave = newSplit[cnt]                        

                        if ( 'mustNotHaveLayers' not in sections[id] ) : 
                            sections[id]['mustNotHaveLayers'] = collections.OrderedDict () 
                        sections[id]['mustNotHaveLayers'][mustNotHave] = True 
                        #print ( "mustNot Have Layer: ", sections[id]['mustNotHaveLayers'] ) 


                    #print ( cnt, newSplit[cnt] ) 
                    cnt += 1
                    

        if ( 0 ) : 
            for mvNum in self.movements : 
                print() 
                print ( "Movement Id: ", mvNum ) 
                print ( "Mood: ", self.movements[mvNum]['mood'] ) 
                print ( "Complexity: ", self.movements[mvNum]['complexity'] ) 
                if ( 1 ) : 
                    print ( "Sections" ) 
                    for secId in self.movements[mvNum]['sectionSettings'] :
                        print ( "Section: ", secId, self.movements[mvNum]['sectionSettings'][secId] ) 
                    

        #sys.exit(0) 
        #Initialize mood and sections
        for mvNum in self.movements : 
            self.movements[mvNum]['SectionsObj'] = Mood ( self.movements[mvNum], self.tempo ) 
            if ( 0 ) : 
                sec = self.movements[mvNum]['SectionsObj'].mood
                print ( "Arrangement for Movement" ) 
                for secId in sec.sections : 
                    print ( "Section: ", secId, "Uniq Mel Id: ", sec.sections[secId]['melId'] ) 
                    uniqCPId = sec.sections[secId]['melId'] 
                    numChordsInPhrase = sec.uniqCPSettings[uniqCPId]['numChords']
                    phNum = 0
                    for chId in sec.sections[secId]['chords'] : 
                        if ( chId % numChordsInPhrase == 0 ) :
                            print() 
                            print ( "\tPhrase: ", phNum + 1, sec.sections[secId]['phrases'][phNum] ) 
                            phNum += 1
                        print ( "\t\tChord: ", chId, sec.sections[secId]['chords'][chId] ) 
                    print() 




        self.printDetails()

        self.populateSections() 


        self.WriteCompositionSettings () 


                
    def printDetails ( self ) : 

        print() 
        for mvNum in self.movements : 
            sectionsObj = self.movements[mvNum]['SectionsObj'].mood
            print ( "Movement: ", mvNum, "Mood: ", self.movements[mvNum]['mood'], "Complexity: ", self.movements[mvNum]['complexity'], "Num Uniq Layers:", sectionsObj.numUniqCPs ) 
            print() 
            print ( "Arrangement for Movement" ) 
            for secId in sectionsObj.sections : 
                tse = sectionsObj.sections[secId]['tse'] 
                print ( "\tSection: ", secId, "Uniq Mel Id: ", sectionsObj.sections[secId]['melId'], "TSE: ", tse  ) 
                uniqCPId = sectionsObj.sections[secId]['melId'] 
                numChordsInPhrase = sectionsObj.uniqCPSettings[uniqCPId]['numChords']
                phNum = 0
                for chId in sectionsObj.sections[secId]['chords'] : 
                    if ( chId % numChordsInPhrase == 0 ) :
                        print() 
                        print ( "\t\tPhrase: ", phNum + 1, sectionsObj.sections[secId]['phrases'][phNum] ) 
                        phNum += 1
                    print ( "\t\tChord: ", chId, sectionsObj.sections[secId]['chords'][chId] ) 
                print() 


    def populateSections ( self ) : 


        DevServer.Server.run ( self.movements ) # this will be a json object that will be passed to the server


        for mvNum in self.movements : 
            sectionsObj = self.movements[mvNum]['SectionsObj'].mood        
            numUniqCPs  = sectionsObj.numUniqCPs  
            self.movements[mvNum]['layers'] = collections.OrderedDict()             

            print ( "numUniqCPs: ", numUniqCPs ) 

            for uniqCPId in range(numUniqCPs) : 
                pl     = sectionsObj.uniqCPSettings[uniqCPId]['pl'] 
                key    = sectionsObj.uniqCPSettings[uniqCPId]['scale'] 
                #bpm    = sectionsObj.uniqCPSettings[uniqCPId]['bpm'] 
                tse    = sectionsObj.uniqCPSettings[uniqCPId]['tse'] 
                cpSeq  = sectionsObj.uniqCPSettings[uniqCPId]['cpSeq'] 
                layers = sectionsObj.layers 
                percussionSettings = sectionsObj.uniqCPSettings[uniqCPId]['percussionSettings'] 


                #if hasattr( sectionsObj.uniqCPSettings[uniqCPId], 'bassRhythm' ) : 

                if ( 'bassRhythm' in sectionsObj.uniqCPSettings[uniqCPId] ) : 
                    bassRhythmOptions = sectionsObj.uniqCPSettings[uniqCPId]['bassRhythm'] #sectionsObj.bassRhythm
                else : 
                    bassRhythmOptions = None 


                mood  = self.movements[mvNum]['mood'] 
                rhythmSpeed = self.movements[mvNum]['rhythmSpeed'] 
                complexity = self.movements[mvNum]['complexity'] 
                
                wbLevers = {
                    'id'          : uniqCPId,

                    'phraseLength': pl,
                    'tse'         : tse, 
                    'primaryScale': key,
                    'bassRhy'     : cpSeq,

                    'mood'        : mood,
                    'complexity'  : complexity, 
                    'rhythmSpeed' : rhythmSpeed,
                    
                    'layers'      : layers, 

                    'bassRhythmOptions' : bassRhythmOptions,

                    'percussionSettings': percussionSettings, 
                    
                    }

                section = Section.Section ( wbLevers ) 
                self.movements[mvNum]['layers'][uniqCPId] = section.run () 

                
            arrangeSections = ArrangeSections ( mvNum, self.movements[mvNum] ) 
            arrangeSections.arrange() 



    def WriteCompositionSettings ( self )  :

        printNotation = True
        foutName = "CompositionSettings" 
        fout = open ( foutName, mode='w' ) 
        

        for mvNum in self.movements : 

            sectionsObj = self.movements[mvNum]['SectionsObj'].mood
            numSections = len(sectionsObj.sections) 

            String = "Movement " + str( mvNum ) + " type promo " + "NumSections " + str( numSections ) + " Mood " + self.movements[mvNum]['mood']  +  "\n"  
            #print ( String ) 
            fout.write ( String ) 

            for secId in sectionsObj.sections : 
                numPhrases = int(sectionsObj.sections[secId]['repCount'])
                uniqCPId = sectionsObj.sections[secId]['melId'] 
                numChordsInPhrase = sectionsObj.uniqCPSettings[uniqCPId]['numChords']
                bpm = sectionsObj.sections[secId]['bpm']
                tse = sectionsObj.uniqCPSettings[uniqCPId]['tse']

                startingMNum = sectionsObj.sections[secId]['startMNum']
                
                String = "SectionNum " + str(secId) + " NumPhrases " + str(numPhrases) + " NumChords " + str(numChordsInPhrase) + " tempo " + str(bpm) + " tse " + str(tse) + " startMNum " + str(startingMNum) + "\n" 
                #print ( String ) 
                fout.write ( String ) 
                phNum = 0
                sectionLayers = []
                for chId in sectionsObj.sections[secId]['chords'] : 
                    if ( chId % numChordsInPhrase == 0 ) :
                        for l in sectionsObj.sections[secId]['phrases'][phNum]['layers'] :
                            sectionLayers.append ( l ) 

                        lyr = str(sectionsObj.sections[secId]['phrases'][phNum]['layers'])
                        lyr = lyr.replace ( " ", "" ) 
                        if ( printNotation ) : 
                            lyr = lyr.replace ( "]", "" )
                            lyr += ",'notationLP','notationRP']"

                        String = "PhraseNum " + str(phNum) + " StartClk " + str(sectionsObj.sections[secId]['phrases'][phNum]['globalStartTick']) + " EndClk " + str(sectionsObj.sections[secId]['phrases'][phNum]['globalEndTick']) + " Density "  + str(sectionsObj.sections[secId]['phrases'][phNum]['density']) + " Layers " + lyr + "\n" 
                        #print ( String ) 
                        fout.write ( String ) 
                        phNum += 1

                sectionLayers = list(set(sectionLayers)) 
                sectionLayers = str(sectionLayers) 
                sectionLayers = sectionLayers.replace ( " ", "" ) 
                if ( printNotation ) : 
                    sectionLayers = sectionLayers.replace ( "]", "" ) 
                    sectionLayers  += ",'notationLP','notationRP']"
                #sectionLayers = sectionLayers.replace ( "[", "" ) 
                #sectionLayers = sectionLayers.replace ( "]", "" ) 
                #sectionLayers = sectionLayers.replace ( "'", "" ) 
                #sectionLayers = sectionLayers.replace ( ",", "" ) 
                        
                fout.write( "SectionLayers " + str(sectionLayers) ) 
                fout.write ( "\n" ) 

        fout.write ( "\n" ) 

        fout.close() ;




    def createSectionsWithUniqueMelodies1 ( self, levers ) : 

        self.wbLevers = collections.OrderedDict()
        for mvNum in range(self.numMovements) : 
            self.wbLevers[mvNum] =  self.element.InitializeWastsonBeatMelodyDetails ( mvNum ) 

        self.uniqLayers = collections.OrderedDict() 


        print() 
        for mvNum in range(self.numMovements) : 
            
            self.uniqLayers[mvNum]  = collections.OrderedDict() 
            print ( "Movement: ", mvNum ) 
            for uniqMelId in self.wbLevers[mvNum] : 
                self.wbLevers[mvNum][uniqMelId] = dict ( self.wbLevers[mvNum][uniqMelId], **levers ) 
                self.wbLevers[mvNum][uniqMelId]['primaryScale'] =  self.wbLevers[mvNum][uniqMelId]['key']
                self.wbLevers[mvNum][uniqMelId]['complexity'] = levers['complexity'][mvNum]
                self.wbLevers[mvNum][uniqMelId]['id'] = uniqMelId
                print ( "Unique Melody: ", uniqMelId, self.wbLevers[mvNum][uniqMelId] ) 
                
                section = Section.Section ( self.wbLevers[mvNum][uniqMelId] )
                section.PrintClassInfo ()                 
                self.uniqLayers[mvNum][uniqMelId] = section.run() 
            print() 


        self.printUniqLayers()
        self.printDetails()


    def replicatePhraseForSections ( self ) : 

        self.CompositionSettingsForMelody = collections.OrderedDict() 

        for mvNum in range(self.numMovements) : 
            midiOutput = CreateMidiFiles.Midi ( self.Movement[mvNum], self.uniqLayers[mvNum], self.LyrTemplateForSections[mvNum] ) 
            self.CompositionSettingsForMelody[mvNum] = midiOutput.ReplicateLayers () 
            

       # for mvNum in range(self.numMovements) : 
       #     self.CompositionSettingsForMelody[mvNum] = HelperFunctions.createMidiEvents ( self.Movement[mvNum], self.uniqLayers[mvNum], self.LyrTemplateForSections[mvNum] ) 
                

    def printUniqLayers ( self ) : 
        for mvNum in range(self.numMovements) : 
            print() 
            print ( "Unique Movement: ", mvNum ) 
            for uniqMelId in self.uniqLayers[mvNum] : 
                print ( "\tUnique Melody Section: ", uniqMelId )                 
                for layer in self.uniqLayers[mvNum][uniqMelId] : 
                    print ( "\t\tLayer: ", layer )               
                    if ( layer in ['melP', 'piano1', 'rhythmChords', 'strings1', 'strings2'] ) :                         
                        if ( 0 ) : 
                            for chordSplit in self.uniqLayers[mvNum][uniqMelId][layer] : 
                                for item in chordSplit : 
                                    print ( "\t\t\tItem: Scale: ", item['scale'], "Chord: ", item['chord'] ) 
                    elif ( layer in ['mel5'] ) : 

                        for mnum in self.uniqLayers[mvNum][uniqMelId][layer]['main'] : 
                            for beatnum in self.uniqLayers[mvNum][uniqMelId][layer]['main'][mnum] : 
                                print ( "\t\t\tMeasure: ", mnum, "Beat: ", beatnum, self.uniqLayers[mvNum][uniqMelId][layer]['main'][mnum][beatnum] )
                            print() 

                    elif (  layer.startswith ( 'drums' ) ) : 

                        if ( 0 ) : 
                            for mnum in self.uniqLayers[mvNum][uniqMelId][layer] : 
                                for item in self.uniqLayers[mvNum][uniqMelId][layer][mnum] : 
                                    print ( "\t\t\tMeasure: ", mnum, "Item: ", item ) 
                                print() 


                    else : 
                        for item in self.uniqLayers[mvNum][uniqMelId][layer] : 
                            if ( 'scale' in item and 'chord' in item ) : 
                                print ( "\t\t\tItem: Scale: ", item['scale'], "Chord: ", item['chord'] ) 

        #sys.exit(0) 

    def WriteCompositionSettings1 ( self )  :

        foutName = "CompositionSettings" 
        fout = open ( foutName, mode='w' ) 

        for mvNum in range(self.numMovements) : 
            for uniqMelId in self.uniqLayers[mvNum] : 
                layer = 'bass1' 
                print ( "\t\tLayer: ", layer,  )               
                for item in self.uniqLayers[mvNum][uniqMelId][layer] : 
                    print ( "\t\t\tItem: Scale: ", item['scale'], "Chord: ", item['chord'] ) 
                    String = "BassId " + str(uniqMelId) + " BassScale " + item['scale'] + " BassChord " + item['chord'] + " BassDuration " + str(item['duration'][0]) + "\n" 
                    fout.write ( String ) 

        
        print() 
        for mvNum in range(self.numMovements) : 
            print() 

            String = "Movement " + str( self.Movement[mvNum]['id']) +  " NumSections " + str( self.Movement[mvNum]['numSections'] ) + " Mood " + self.element.getSubMood() +  " Element " +  self.element.getElement() + " Genre " + self.element.getGenre() +  "\n"  
            fout.write ( String ) 
                    
            for sec in self.Movement[mvNum]['Sections'] : 
                String = "SectionNum " + str(sec ) + " Type " + self.Movement[mvNum]['Sections'][sec]['type'] +  " tse " +  self.Movement[mvNum]['Sections'][sec]['tse'] +  " tempo " +  str( self.Movement[mvNum]['Sections'][sec]['bpm'] ) +  " NumPhrases " + str(self.Movement[mvNum]['Sections'][sec]['repCount'] ) + " NumMeasuresPerPhrase " + str(self.Movement[mvNum]['Sections'][sec]['phraseLength'] ) +  " StartingMeasureNum " + str( self.Movement[mvNum]['Sections'][sec]['startMNum'] ) +  " EndingMeasureNum " + str( self.Movement[mvNum]['Sections'][sec]['endMNum'] ) + "\n" 
                fout.write ( String ) 


        fout.write ( "\n" ) 

        if ( len(self.CompositionSettingsForMelody) == 0 ) : 
            fout.close() ;
            return 

        for mvNum in range(self.numMovements) : 
            for sec in self.Movement[mvNum]['Sections'] : 
                if ( sec not in self.CompositionSettingsForMelody[mvNum] ) : 
                    continue
                for ph in self.CompositionSettingsForMelody[mvNum][sec] :  
                    String = "StartofSection " + str(sec ) + " PhraseNum " + str( ph) + " Clock " + str( self.CompositionSettingsForMelody[mvNum][sec][ph]['clock'] ) + " Mute " + str(  self.CompositionSettingsForMelody[mvNum][sec][ph]['mute'] ) + " MaxPitch " + str(  self.CompositionSettingsForMelody[mvNum][sec][ph]['maxPitch'] ) + " MinPitch " + str(  self.CompositionSettingsForMelody[mvNum][sec][ph]['minPitch'] ) + "\n" 
                    fout.write ( String ) 
        fout.close() ;


    def ReadCompositionSettings1 ( self ) : 
        
        finName = "CompositionSettings" 
        fin = open ( finName, mode='r' ) 

        compositionSettings = collections.OrderedDict() 
        movementSettings = collections.OrderedDict() 

        for line in fin : 
            line = line.rstrip() 

            #print ( "line: ", line ) 
            
            if ( line.startswith ( "Movement" ) ) : 

                data = line.split () 
                for item in range(0, len(data), 2)  : 
                    if ( data[item] == 'Movement' ) : 
                        mvNum = int(data[item+1] ) 
                        compositionSettings[mvNum] = collections.OrderedDict() 
                        movementSettings[mvNum] = collections.OrderedDict() 
                    elif ( data[item] == 'Mood' ) : 
                        movementSettings[mvNum]['mood'] = data[item+1]
                    elif ( data[item] == 'Element' ) : 
                        movementSettings[mvNum]['element'] = data[item+1]
                    elif ( data[item] == 'Genre' ) : 
                        movementSettings[mvNum]['genre'] = data[item+1]

            elif ( line.startswith ( "SectionNum" ) ) : 

                data = line.split () 
                for item in range(0, len(data), 2)  : 
                    #print ( item, data[item],  data[item+1] ) 
                    if ( data[item] == 'SectionNum' ) : 
                        secNum = int(data[item+1] ) 
                        compositionSettings[mvNum][secNum] = collections.OrderedDict() 
                        movementSettings[mvNum][secNum]    = collections.OrderedDict() 
                    elif ( data[item] == 'NumPhrases' ) : 
                        numPhrases = int(data[item+1])
                        for ph in range(numPhrases) : 
                            compositionSettings[mvNum][secNum][ph] = {'clock': 0, 'mute': False }
                            #print ( "Section: ", secNum, "Phrase Num: ", ph ) 
                    elif ( data[item] == 'Type' ) : 
                        movementSettings[mvNum][secNum]['type'] = data[item+1]
                    elif ( data[item] == 'tse' ) : 
                        movementSettings[mvNum][secNum]['tse'] = data[item+1]
                    elif ( data[item] == 'tempo' ) : 
                        movementSettings[mvNum][secNum]['tempo'] = data[item+1]
  
            elif ( line.startswith ( "StartofSection" ) ) : 

                data = line.split () 
                for item in range(0, len(data), 2)  : 
                    #print ( "SoS: ", item, data[item],  data[item+1] ) 
                    if ( data[item] == 'StartofSection' ) : 
                        secNum = int(data[item+1] ) 
                        #print ( "Sec Num: ", secNum ) 
                    elif ( data[item] == 'PhraseNum' ) : 
                        phNum = int(data[item+1] ) 
                        #print ( "Phrase Num: ", phNum ) 
                    elif ( data[item] == 'Clock' ) : 
                        compositionSettings[mvNum][secNum][phNum]['clock'] = int(data[item+1] )  
                    elif ( data[item] == 'Mute' ) : 
                        compositionSettings[mvNum][secNum][phNum]['mute'] = data[item+1]
                        

        fin.close() 


        print() 
        print() 
        for mvNum in compositionSettings : 
            print ( "Movement: ", mvNum, "Mood: ", movementSettings[mvNum]['mood'], "Element: ", movementSettings[mvNum]['element'], "Genre: ", movementSettings[mvNum]['genre'] )
            for sec in compositionSettings[mvNum] : 
                print ( "Section: ", sec, "Type: ",  movementSettings[mvNum][sec]['type'], "Time Signature: ",  movementSettings[mvNum][sec]['tse'], "Tempo: ",  movementSettings[mvNum][sec]['tempo'] ) 
                for ph in compositionSettings[mvNum][sec] : 
                    print ( "phrase: ", ph, "Clock: ", compositionSettings[mvNum][sec][ph]['clock'], "Mute: ", compositionSettings[mvNum][sec][ph]['mute'] ) 




def run () : 
    
    iniFile = sys.argv[1]
    print ( iniFile ) 
    
    try : 
        tempo = int(sys.argv[2])
    except : 
        tempo = None 
    print ( "tempo: ", tempo ) 

    #random.seed ( 10 ) 
    #random.seed ( 50 ) 

    #random.seed ( 130 ) #fails
    #random.seed ( 10 )
    #random.seed ( 10 )

    rmCmd = "rm -rf WB*.mid WB*.py" 
    os.system ( rmCmd ) 

    #skeleton = Template( "Skeleton/Inspire.ini" ) 
    skeleton = Template( iniFile, tempo ) 



def run1 () : 


    #random.seed ( 21 ) 
    #random.seed ( 65 ) 

    rmCmd = "rm -rf WB*.mid WB*.py" 
    os.system ( rmCmd ) 

    complexityKnob  = [ 'simple' ]
    complexityKnob  = [ 'complex' ]
    complexityKnob  = [ 'semi_complex' ]
    complexityKnob  = [ 'super_simple', 'complex1' ] # len(complexityKnob) signifies number of movements
    complexityKnob  = [ 'super_simple' ]

    mood         = 'Calm'
    element      = 'water'
    genre        = 'Classical'
    rhythmSpeed  = 'slow' # can be fast and medium

    mood         = 'Epic'
    element      = ''
    genre        = 'General' 
    rhythmSpeed  = 'medium' # can be fast and slow

    mood         = 'Inspire'
    element      = ''
    genre        = 'General' 
    rhythmSpeed  = 'medium' # can be fast and slow


    levers = {
        'mood'        : mood, 
        'element'     : element,
        'mood+element': mood + element,
        'genre'       : genre,
        'complexity'  : complexityKnob, 
        'rhythmSpeed' : rhythmSpeed,
        #'configFile'  : 'ConfigFile.ini', 
        'numChords'   : random.choice ( [1, 4, 2]),   # -1 indicates, let watson decide
        }


    skeleton = Template(  levers['mood+element'], levers['genre'], levers['complexity'] ) 
    #skeleton = Template( 'Calmwater', 'Classical', [ 'simple', 'complex1']  ) 

    

    skeleton.createSectionsWithUniqueMelodies ( levers )


    skeleton.replicatePhraseForSections () 
    skeleton.WriteCompositionSettings () 
    skeleton.ReadCompositionSettings () 


    sys.exit(0) 


    pl = 4
    tse = '3/4'
    primaryScale = 'CMajor'
    wbLevers = {
        'mood'        : mood,
        'element'     : element, 
        'genre'       : genre,
        'complexity'  : complexityKnob, 
        'rhythmSpeed' : rhythmSpeed,
        'phraseLength': pl,
        'tse'         : tse, 
        'primaryScale': primaryScale 
        }





if __name__ == '__main__' : 


    skeleton = Template( 'Calmwater', 'Classical', [ 'simple', 'complex1']  ) 




    

