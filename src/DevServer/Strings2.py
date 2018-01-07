from __future__ import print_function
from itertools import chain

import sys
import random
import collections

import Constants
import MusicTheory



prnFlag = False

class Strings2 () : 
    '''
    '''

    def __init__ ( self, wbLevers, chordDict ) : 

        self.desc = 'strings2'
        self.chordDict = chordDict 
        
        self.StringClass = collections.OrderedDict()
        self.StringClass['loStrings'] = collections.OrderedDict()
        self.StringClass['loStrings'][0] = { 'desc': 'doubleBass', 'numNotes': 1, 'minPitch': 36, 'minOctave': 3, 'maxPitch': 60, 'maxOctave': 5, 'repeats': 1 }
        self.StringClass['loStrings'][1] = { 'desc': 'cello',     'numNotes': 1, 'minPitch': 48, 'minOctave': 4, 'maxPitch': 72, 'maxOctave': 6, 'repeats': 1 }

        self.StringClass['midStrings'] = collections.OrderedDict()        
        self.StringClass['midStrings'][0] = {'desc': 'viola',   'minPitch': 60, 'minOctave': 5, 'maxPitch': 84, 'maxOctave': 7, 'numNotes': 1, 'repeats': 1 } 
        self.StringClass['midStrings'][1] = {'desc': 'violin2', 'minPitch': 60, 'minOctave': 5, 'maxPitch': 88, 'maxOctave': 7, 'numNotes': self.StringClass['midStrings'][0]['numNotes'], 'repeats': 1 } 


        self.StringClass['hiStrings'] = collections.OrderedDict()        
        self.StringClass['hiStrings'][0] = {'desc': 'violin1',  'minPitch': 74, 'minOctave': 6, 'maxPitch': 103, 'maxOctave': 8, 'numNotes': self.StringClass['midStrings'][0]['numNotes'], 'repeats': 1 } 

        self.StringClass['arpStrings'] = collections.OrderedDict()        
        self.StringClass['arpStrings'][0] = {'desc': 'arp0', 'minPitch': 65, 'minOctave': 5, 'maxPitch': 88, 'maxOctave': 7, 'numNotes': random.randint(1,4), 'repeats': 1 }         
        self.StringClass['arpStrings'][1] = {'desc': 'arp1', 'minPitch': 65, 'minOctave': 5, 'maxPitch': 88, 'maxOctave': 7, 'numNotes': random.randint(1,4), 'repeats': 1 }         
        self.StringClass['arpStrings'][2] = {'desc': 'arp2', 'minPitch': 65, 'minOctave': 5, 'maxPitch': 88, 'maxOctave': 7, 'numNotes': random.randint(1,4), 'repeats': 1 }         


        self.StringClass['leftPianoBass'] = collections.OrderedDict()        
        self.StringClass['leftPianoBass'][0] = {'desc': 'leftPianoBass', 'minPitch': 24, 'minOctave': 2, 'maxPitch': 48, 'maxOctave': 4, 'numNotes': 2, 'repeats': 1 }

        self.StringClass['rightPiano'] = collections.OrderedDict()        
        self.StringClass['rightPiano'][0] = {'desc': 'rp0', 'minPitch': 55, 'minOctave': 4, 'maxPitch': 79, 'maxOctave': 6, 'numNotes': random.randint(4,4), 'repeats': 1 }   #repeats indicates how many times a chor tone can repeat
        self.StringClass['rightPiano'][1] = {'desc': 'rp1', 'minPitch': 55, 'minOctave': 4, 'maxPitch': 79, 'maxOctave': 6, 'numNotes': random.randint(4,4), 'repeats': 1 }   #repeats indicates how many times a chor tone can repeat
        self.StringClass['rightPiano'][2] = {'desc': 'rp2', 'minPitch': 55, 'minOctave': 4, 'maxPitch': 79, 'maxOctave': 6, 'numNotes': random.randint(4,4), 'repeats': 1 }   #repeats indicates how many times a chor tone can repeat
        self.StringClass['rightPiano'][3] = {'desc': 'rp3', 'minPitch': 55, 'minOctave': 4, 'maxPitch': 79, 'maxOctave': 6, 'numNotes': 3, 'repeats': 0 }   #repeats indicates how many times a chor tone can repeat

        self.StringClass['rightPiano2'] = collections.OrderedDict()        
        self.StringClass['rightPiano2'][0] = {'desc': 'rp0', 'minPitch': 55, 'minOctave': 4, 'maxPitch': 79, 'maxOctave': 6, 'numNotes': random.randint(1,4), 'repeats': 1 }   #repeats indicates how many times a chor tone can repeat
        self.StringClass['rightPiano2'][1] = {'desc': 'rp1', 'minPitch': 55, 'minOctave': 4, 'maxPitch': 79, 'maxOctave': 6, 'numNotes': random.randint(1,4), 'repeats': 1 }   #repeats indicates how many times a chor tone can repeat
        self.StringClass['rightPiano2'][2] = {'desc': 'rp2', 'minPitch': 55, 'minOctave': 4, 'maxPitch': 79, 'maxOctave': 6, 'numNotes': random.randint(1,4), 'repeats': 1 }   #repeats indicates how many times a chor tone can repeat



        if ( prnFlag ) : 
            self.PrintClassInfo() 

        if ( 0 ) : 
            for key in chordDict : 
                print ( key , chordDict[key]) 
            print()

        self.consolidateChords ()

        if ( 0 ) : 
            for key in self.consolidatedChords : 
                print ( key, self.consolidatedChords[key] ) 
            print()

        self.speed = 'slow' # why slow for stings always, because we dont want the chords to be split into multiple segments. We want to sustain the chord notes for as long as we can 

        self.trainedData = collections.OrderedDict() 



    def consolidateChords ( self ) :
        
        self.consolidatedChords = collections.OrderedDict ()
        cnt = 0 
        prevChord = ''
        for chid in range(len(self.chordDict)) :
            currChord =  self.chordDict[chid]['chord'] 
            currDuration = self.chordDict[chid]['duration'] 
            if ( chid == 0 ) : 
                prevChord    = self.chordDict[chid]['chord'] 
                prevDuration = self.chordDict[chid]['duration'] 
                startClk       = 0 
            elif ( currChord == prevChord ) : 
                prevDuration += currDuration
            else : 
                self.consolidatedChords[cnt] = { 'chord': prevChord, 'duration': prevDuration, 'Clk': [ startClk, startClk + prevDuration] }
                startClk  += prevDuration
                cnt += 1
                prevChord = currChord
                prevDuration = currDuration


        self.consolidatedChords[cnt] = { 'chord': prevChord, 'duration': prevDuration, 'Clk':  [ startClk, startClk + prevDuration]  }


    def run ( self ) : 

        for chId in self.consolidatedChords : 
            chord = self.consolidatedChords[chId]['chord'] 

            if ( chId != 0 ) :                 
                chordProgressionChoice = random.choice ( [ 'leadingVoice',  'leadingVoice', 'any',  'leadingVoice', 'any', 'planing', 'leadingVoice'] ) 
                if ( 0 ) : 
                    print ( "chordProgressionChoice: ", chordProgressionChoice )             
            
            else : 
                chordProgressionChoice = 'initial' 


            self.consolidatedChords[chId]['cpChoice'] = chordProgressionChoice



            if ( 0 ) :
                print ( "Chord Id: ", chId, "chordProgression choice: ", chordProgressionChoice ) 

            if ( chId == 0 or chordProgressionChoice == 'any' ) : 

                for strClass in self.StringClass :  # strClass can be 'loStrings', 'midStrings', 'hiStrings' 'arpStrings'

                    self.consolidatedChords[chId][strClass] = collections.OrderedDict() 
                    if ( strClass == 'arpStrings' ) : 
                        chordList    = MusicTheory.ArpChords[chord]
                    elif ( strClass == 'leftPianoBass' ) : 
                        chordList = [ MusicTheory.AllChords[chord][0] ] # only the home note
                    else : 
                        chordList = MusicTheory.AllChords[chord]
                

                    for instId in self.StringClass[strClass] : # instid is intsrument id and can be 0, 1 or 2
                                     
                        #if ( instId == 0 ) : # if it's the first instrument in its class, figure out the notes that will be played for this class
                        if ( instId == 0 or not( strClass =='loStrings' or strClass =='midStrings' or strClass =='hiStrings') ) : # if it's the first instrument in its class, figure out the notes that will be played for this class
                            noteIndex = []                             
                            for notes in range(self.StringClass[strClass][instId]['numNotes']) :                                 
                                if ( notes == 0 and strClass == 'arpStrings' ) : 
                                    indexId = random.randint(0, 2)
                                else : 
                                    while ( True ) : 
                                        indexId = random.randint(0, len(chordList)-1)
                                        #if ( strClass == 'arpStrings' ) : 
                                            #print ( "str class: ", strClass, "indexId: ", indexId, "count: ", noteIndex.count(indexId), "Note Index list: ", noteIndex , "repeats: ", self.StringClass[strClass][instId]['repeats'] ) 
                                        if ( noteIndex.count(indexId) <= self.StringClass[strClass][instId]['repeats'] ) : 
                                            break 

                                noteIndex.append (indexId ) 
                        if ( 0 and (strClass == 'arpStrings' or strClass == 'rightPiano') ) : 
                            print ( "ChordId: ", chId, "Desc: ", self.StringClass[strClass][instId]['desc'], "InstId: ", instId, "noteIndex: ", noteIndex, "numNotes: ", self.StringClass[strClass][instId]['numNotes'] ) 
                        self.consolidatedChords[chId][strClass][instId] =  { 'desc': self.StringClass[strClass][instId]['desc'], 'noteIndex': noteIndex, 'items': [] } 
                        pitches = [] 
                        for noteId in noteIndex : 
                            while ( True ) :
                                note   = chordList[noteId]
                                octave = random.randint ( self.StringClass[strClass][instId]['minOctave'],  self.StringClass[strClass][instId]['maxOctave'] ) 
                                indexId  = MusicTheory.NotesToPitch[note] 
                                pitch  = ( octave * 12 ) +  indexId
                                #print ( self.StringClass[strClass][instId] ) 
                                #print ( "Note: ", note, "octave: ", octave, "Pitch: ", pitch, "Pitches: ",pitches, self.consolidatedChords[chId][strClass][instId]['noteIndex'] ) 

                                if ( pitch > self.StringClass[strClass][instId]['maxPitch'] ) : 
                                    pitch -= 12
                                    octave = pitch // 12
                                elif ( pitch < self.StringClass[strClass][instId]['minPitch'] ) : 
                                    pitch += 12
                                    octave = pitch // 12
                                
                                if ( pitch not in pitches ) : 
                                    pitches.append(pitch) 
                                    break 

                            self.consolidatedChords[chId][strClass][instId]['items'].append ( { 'note': note, 'pitch': pitch, 'octave': octave, 'consolidateFlag': False, 'velocity': random.randint(50,80) } ) 
                            
                    

            elif ( chordProgressionChoice == 'planing' ) :  # use the same note indices as the previous chord

                for strClass in self.StringClass :  # strClass can be 'loStrings', 'midStrings', 'hiStrings'

                    self.consolidatedChords[chId][strClass] = collections.OrderedDict() 
                    if ( strClass == 'arpStrings' ) : 
                        chordList = MusicTheory.ArpChords[chord]
                    elif ( strClass == 'leftPianoBass' ) : 
                        chordList = [ MusicTheory.AllChords[chord][0] ] # only the home note
                    else : 
                        chordList = MusicTheory.AllChords[chord]
                    
                    for instId in self.StringClass[strClass] : # instid is intsrument id and can be 0, 1 or 2

                        self.consolidatedChords[chId][strClass][instId] =  {  'desc': self.StringClass[strClass][instId]['desc'],  'noteIndex':  self.consolidatedChords[chId-1][strClass][instId]['noteIndex'], 'items': [] } 
                        pitches = [] 
                        for noteId in self.consolidatedChords[chId][strClass][instId]['noteIndex'] :

                            if noteId > len(chordList) - 1 :  # to account fo lack of seventh note in triad
                                noteId = 0 

                            tryFor100Times = 0 
                            while ( True ) : 
                                if ( 0 ) :
                                    print ( "ChordId: ", chId, "NoteId", noteId, "chordList: ", chordList, "str class: ", strClass, "Note Index list: ", self.consolidatedChords[chId][strClass][instId]['noteIndex'], "prev noteIndex list: ",  self.consolidatedChords[chId-1][strClass][instId]['noteIndex'] ) 


                                note   = chordList[noteId]
                                octave = random.randint ( self.StringClass[strClass][instId]['minOctave'],  self.StringClass[strClass][instId]['maxOctave'] ) 
                                indexId  = MusicTheory.NotesToPitch[note] 
                                pitch  = ( octave * 12 ) +  indexId
                                #print ( self.StringClass[strClass][instId] ) 
                                #print ( "Note: ",note,"octave: ",octave, "Pitch: ", pitch, "Pitches: ", pitches, self.consolidatedChords[chId][strClass][instId]['noteIndex']  ) 
                                tryFor100Times += 1

                                if ( pitch > self.StringClass[strClass][instId]['maxPitch'] ) : 
                                    pitch -= 12
                                    octave = pitch // 12
                                elif ( pitch < self.StringClass[strClass][instId]['minPitch'] ) : 
                                    pitch += 12
                                    octave = pitch // 12
                                                                    
                                if ( pitch not in pitches or tryFor100Times == 100  ) :                                     
                                    if ( tryFor100Times == 100 ) : 
                                        print ( "Tried for 100 times. Now exiting!" ) 
                                        #print ( "Note: ",note,"octave: ",octave, "Pitch: ", pitch, "Pitches: ", pitches, self.consolidatedChords[chId][strClass][instId]['noteIndex']  ) 
                                    pitches.append(pitch) 
                                    break 

                            self.consolidatedChords[chId][strClass][instId]['items'].append ( { 'note': note, 'pitch': pitch, 'octave': octave, 'consolidateFlag': False, 'velocity': random.randint(50,80) } )                             


            elif ( chordProgressionChoice == 'leadingVoice' ) :  # for every note played in the previous chord, find next closest note for this chord and slide into it 

                for strClass in self.StringClass :  # strClass can be 'loStrings', 'midStrings', 'hiStrings'

                    self.consolidatedChords[chId][strClass] = collections.OrderedDict()                     
                    if ( strClass == 'arpStrings' ) : 
                        chordList = MusicTheory.ArpChords[chord]
                    elif ( strClass == 'leftPianoBass' ) : 
                        chordList = [ MusicTheory.AllChords[chord][0] ] # only the home note
                    else : 
                        chordList = MusicTheory.AllChords[chord]

                    for instId in self.StringClass[strClass] : # instid is intsrument id and can be 0, 1 or 2

                        self.consolidatedChords[chId][strClass][instId] =  {  'desc': self.StringClass[strClass][instId]['desc'],  'noteIndex': [], 'items': [] } 

                        for noteid in range(len(self.consolidatedChords[chId-1][strClass][instId]['items'])) :
                            note  = self.consolidatedChords[chId-1][strClass][instId]['items'][noteid]['note']
                            pitch = self.consolidatedChords[chId-1][strClass][instId]['items'][noteid]['pitch']
                            adder = 1
                            while ( note not in chordList ) : 
                                pitchA = pitch + adder
                                modA   = pitchA % 12 
                                noteA  = MusicTheory.pitchToNotes[modA] 

                                pitchB = pitch - adder
                                modB   = pitchB % 12 
                                noteB  = MusicTheory.pitchToNotes[modB] 

                                if ( noteA in chordList ) : 
                                    note  = noteA
                                    pitch = pitchA 
                                    break 

                                if ( noteB in chordList ) : 
                                    note  = noteB
                                    pitch = pitchB
                                    break 
                                adder += 1

                            octave = pitch // 12
                            noteIndex = chordList.index(note)
                            self.consolidatedChords[chId][strClass][instId]['noteIndex'].append ( noteIndex ) 
                            self.consolidatedChords[chId][strClass][instId]['items'].append ( { 'note': note, 'pitch': pitch, 'octave': octave, 'consolidateFlag': False,  'velocity': random.randint(50,80) } )                             


        if ( 0 ) : 
            for chId in self.consolidatedChords : 
                chord = self.consolidatedChords[chId]['chord'] 
                print ( "Chord Id : ", chId, "Chord: " , chord, self.consolidatedChords[chId]['cpChoice'], "Duration:",  self.consolidatedChords[chId]['duration'], "Clk:",  self.consolidatedChords[chId]['Clk'] ) 
                for strClass in self.StringClass :  # strClass can be 'loStrings', 'midStrings', 'hiStrings'
                    if ( strClass != 'rightPiano' ) : 
                        continue

                    for instId in self.StringClass[strClass] : # instid is intsrument id and can be 0, 1 or 2

                        for item in self.consolidatedChords[chId][strClass][instId]['items'] : 

                            print ( "String Class: ", strClass, "Instrument Id: ", instId, "Desc: ", self.consolidatedChords[chId][strClass][instId]['desc'], 'NoteIndex: ', self.consolidatedChords[chId][strClass][instId]['noteIndex'], "Note: ", item['note'], "Pitch:", item['pitch'], "octave:", item['octave'], "checked: ", item['consolidateFlag'] ) #
                    print()
                print()
            print()

        #sys.exit(0) 

        # further consolidate chords
        self.StringEvents = collections.OrderedDict()
        glbClk     = 0
        numChords  = len(self.consolidatedChords)

        for strClass in self.StringClass :  # strClass can be 'loStrings', 'midStrings', 'hiStrings'

            self.StringEvents[strClass] = collections.OrderedDict()

            for instId in self.StringClass[strClass] : # instid is intsrument id and can be 0, 1 or 2

                self.StringEvents[strClass][instId] = []
                desc = self.StringClass[strClass][instId]['desc']

                for chId in self.consolidatedChords : 
                    for item in self.consolidatedChords[chId][strClass][instId]['items'] : 

                        if ( item['consolidateFlag'] ) : #item already accounted for.
                            continue

                        currStartClk = self.consolidatedChords[chId]['Clk'][0] 
                        currEndClk   = self.consolidatedChords[chId]['Clk'][1] 

                        for nextChId in range( chId + 1, numChords ) : 
                            extensionFound = False                            
                            for nextItem in self.consolidatedChords[nextChId][strClass][instId]['items'] : 
                                if ( nextItem['consolidateFlag'] ) : #item already accounted for.
                                    continue
                                if ( nextItem['pitch'] == item['pitch'] ) : 
                                    extensionFound = True
                                    nextItem['consolidateFlag'] = True
                                    currEndClk   = self.consolidatedChords[nextChId]['Clk'][1] 

                            if ( not extensionFound ) : 
                                break 
                        


                        self.StringEvents[strClass][instId].append ( { 'desc': desc, 'event': 'on',   'note': item['note'], 'pitch': item['pitch'], 'octave': item['octave'], 'Clk': currStartClk, 'velocity': item['velocity'] } ) 
                        self.StringEvents[strClass][instId].append ( { 'desc': desc, 'event': 'off',  'note': item['note'], 'pitch': item['pitch'], 'octave': item['octave'], 'Clk': currEndClk, 'velocity': 0 } ) 

            
        for strClass in self.StringEvents :  # strClass can be 'loStrings', 'midStrings', 'hiStrings'
                
            for instId in self.StringEvents[strClass] : # instid is intsrument id and can be 0, 1 or 2

                self.StringEvents[strClass][instId] = sorted ( self.StringEvents[strClass][instId], key = lambda x: x['Clk'] ) 
                
                if ( 0 ) : 
                    print() 
                    print ( "String Class: ", strClass, "InstId: ", instId, "Desc: ", self.StringEvents[strClass][instId][0]['desc'] ) 
                    for ev in self.StringEvents[strClass][instId] : 
                        print ( ev ) 

                glbClk = 0 
                for ev in range(len(self.StringEvents[strClass][instId])) : 
                    self.StringEvents[strClass][instId][ev]['midiClk'] = self.StringEvents[strClass][instId][ev]['Clk'] - glbClk
                    self.StringEvents[strClass][instId][ev]['pitch'] = "midi." + self.StringEvents[strClass][instId][ev]['note'] + '_' + str(self.StringEvents[strClass][instId][ev]['octave'])
                    glbClk = self.StringEvents[strClass][instId][ev]['Clk']


                if ( 0 and ( strClass == 'arpStrings'  or strClass == 'rightPiano' ) ) : 
                    print() 
                    print ( "String Class: ", strClass, "InstId: ", instId, "Desc: ", self.StringEvents[strClass][instId][0]['desc'] ) 
                    for ev in self.StringEvents[strClass][instId] : 
                        print ( ev ) 



        #sys.exit(0)
        return ( self.StringEvents ) 


    def PrintClassInfo ( self ) :
        print ( )
        print ( "Layer Description: ", self.desc ) 
        print () 

