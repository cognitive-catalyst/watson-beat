from __future__ import print_function

from Arranging.ArrangeSections import *
from Moods.Mood import Mood


import re
import os
import sys
import json
import random
import Section
import argparse
import requests
import DevServer.Server



class Template : 


    def __init__ ( self, iniFname, midiFilePath, outDir,oneMidiPerLayer) : 
 
        self.tempo = None           
        self.midiFilePath = midiFilePath
        self.outDir = outDir
        self.ReadIniFile ( iniFname ) 
        self.oneMidiPerLayer = oneMidiPerLayer

        #Initialize mood and sections
        for mvNum in self.movements : 
            self.movements[mvNum]['SectionsObj'] = Mood ( self.movements[mvNum], self.tempo ) 

        self.populateSections() 

        self.WriteCompositionSettings () 


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


        wbClientData = collections.OrderedDict () 
        for mvNum in self.movements : 
            sectionsObj = self.movements[mvNum]['SectionsObj'].mood        
            numUniqCPs  = sectionsObj.numUniqCPs  

            wbClientData[mvNum] = collections.OrderedDict () 

            print ( "numUniqCPs: ", numUniqCPs ) 

            for uniqCPId in range(numUniqCPs) : 


                wbClientData[mvNum][uniqCPId] = collections.OrderedDict () 

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

                wbClientData[mvNum][uniqCPId]['wbLevers'] = wbLevers



        # Call the machine learning
        mlResponse = DevServer.Server.run ( json.dumps( wbClientData ), self.midiFilePath ) 
        wbServerData = collections.OrderedDict( json.loads( mlResponse ) )

        #print ( "wbServerResponse text : ", wbServerResponse.text ) 


        for mvNum in self.movements : 
            sectionsObj = self.movements[mvNum]['SectionsObj'].mood        
            numUniqCPs  = sectionsObj.numUniqCPs  
            self.movements[mvNum]['layers'] = collections.OrderedDict()             

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

                section = Section.Section ( wbLevers, wbServerData[str(mvNum)][str(uniqCPId)] ) 
                self.movements[mvNum]['layers'][uniqCPId] = section.run () 

                
            arrangeSections = ArrangeSections ( mvNum, self.movements[mvNum], self.outDir ,self.oneMidiPerLayer) 
            arrangeSections.arrange() 



    def WriteCompositionSettings ( self )  :

        printNotation = True
        foutName = self.outDir + "CompositionSettings" 
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

def usage() :
    usage =  "\nUsage: python wbDev.py -i INI-File -m MIDI-File -o outputdir\n"
    usage += "Example 1: python wbDev.py\n" 
    usage += "Example 1 uses the default Ini file Ini/Space.ini and the default midi file Midi/mary.mid and outdir\n\n" 
    usage += "Example 2: python wbDev.py -i Ini/ReggaePop.ini -m Midi/mary.mid -o /User/Fred/data/tmp/ \n" 
    print ( usage ) 

    sys.exit(0) 

def run () : 

    print("in skeleton")
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', action='store',
                        dest='iniFile',
                        default='Ini/Space.ini',
                        help='Store the ini File')

    parser.add_argument('-m', action='store',
                        dest='midiFilePath',
                        default='Midi/mary.mid',
                        help='Midi File Path')

    parser.add_argument('-o', action='store',
                        dest='outputFilePath',
                        default='./output/',
                        help='Output File Path')

    parser.add_argument('-l', action='store_true',
                        dest='oneMidiPerLayer',
                        help="One midi per layer"  ) 

    parser.add_argument('-u', action='store_true',
                        dest='usage',
                        help="usage"  )
    
    results = parser.parse_args()

    if ( results.usage ) : 
        usage() 


    if not os.path.isfile(results.iniFile) :
        # ini file does not exist
        print ( "\nIncorrect Ini File Path\nReverting to default ini file" )

    if not os.path.isfile(results.midiFilePath) :
        # ini file does not exist
        print ( "\nIncorrect Midi File Path\nReverting to default midi file" )

    if not os.path.exists(results.outputFilePath) :
        # output director does not exist
        os.makedirs( results.outputFilePath ) 

    print('iniFile          = {!r}'.format(results.iniFile ))
    print('midiFile         = {!r}'.format(results.midiFilePath ))
    print('outputDir        = {!r}'.format(results.outputFilePath ))
    print('layerpermidi        = {!r}'.format(results.oneMidiPerLayer ))


    rmCmd = "rm -rf {}/WB*.mid {}/WB*.py".format( results.outputFilePath, results.outputFilePath ) 
    os.system ( rmCmd ) 

    #random.seed ( 10 )

    skeleton = Template( results.iniFile, results.midiFilePath, results.outputFilePath,results.oneMidiPerLayer) 



