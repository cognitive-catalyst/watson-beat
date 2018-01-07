from __future__ import print_function

import os
import sys
import mido
import time
import math
import datetime
import threading
import collections
import MusicTheory


class RecordMidi : 

    def __init__ ( self ) : 
        self.messagesFromMidiInstrument = {} 
        self.midiMessagesNoOverlaps = {} 
        self.midiMessages = {} 
        self.initialClk = 0
        self.phraseLength = 4
    


        self.tsInfo = { 'tsNumerator': 4, 'tsDenominator': 4, 'measureLength': 1920, 'resolution': 480, 'format':0 , 'bpm': 120 } 

        self.oneBeatInSeconds           = 60.0 / self.tsInfo['bpm'] 
        self.oneBeatInMilliSeconds      = round ( self.oneBeatInSeconds*1000, 3 ) 
    

        self.quarterNoteInBeats         = float ( ( (1/4.0) ) / (1.0/self.tsInfo['tsDenominator']) ) 
        self.quarterNoteInSeconds       = self.quarterNoteInBeats *  self.oneBeatInSeconds 
        self.quarterNoteInMilliSeconds  = round ( self.quarterNoteInSeconds*1000, 3 )  

        # resolution = ppq = pulses per quarter note = ticks per quarter note
        self.oneTickInSeconds      = round ( ( self.quarterNoteInSeconds / 480 ) , 7 )
        self.oneTickInMilliSeconds = round ( self.oneTickInSeconds*1000, 3 )  
        
        print ( "1 Tick in Seconds: ", self.oneTickInSeconds ) 
        print ( "1 Tick in Milli Seconds: ", self.oneTickInMilliSeconds ) 


        self.oneSecondInTicks      = round ( 1.0/self.oneTickInSeconds, 0 ) 
        self.oneMilliSecondInTicks = round ((1.0/self.oneTickInMilliSeconds), 2 ) 


        print ( "1 Second in Ticks: ", self.oneSecondInTicks ) 
        print ( "1 Milli Seconds in Ticks: ", self.oneMilliSecondInTicks ) 
    
        self.ticksForPhraseLength = self.tsInfo['measureLength'] * self.phraseLength
        self.secondsForPhraseLength = int ( self.ticksForPhraseLength * self.oneTickInSeconds )
    
        print ( "Phrase Length: ", self.phraseLength, "Num Seconds for Phrase: ", self.secondsForPhraseLength ) 

        #sys.exit(0) 


    def run ( self ) : 
        print ( "Initial Clock: ", self.initialClk ) 
        

        mido.set_backend('mido.backends.rtmidi')
        inport = mido.open_input()

        print ( "Time: ", time.time() ) 


        try:
            initialNotePlayed = False
            numNotes = 0 
            endRecording = False
            with mido.open_input() as port:
                print('Using {}'.format(port))

                print("Initial Clk: ", self.initialClk, "Waiting for messages..." ) 
                                
                for message in port:

                    if ( not initialNotePlayed and message.type == 'note_on' ) : 
                        initialNotePlayed = True                    
                        self.initialClk = message.time
                        print ( "\nStarted Recording" ) 
                        print("First Note Played, Initial Clk: ", self.initialClk ) 

                    if ( message.time - self.initialClk >= self.secondsForPhraseLength )  :
                        print ( "Initial Clk: ", self.initialClk, "Current Time: ", message.time, self.phraseLength, "measures recorded: ", "Number of seconds recorded: ", self.secondsForPhraseLength, "Stop Recording" ) 
                        endRecording = True
                        break 


                    print ( message ) 
                    if ( message.type == 'note_on' or message.type == 'note_off' ) :                         
                        if ( message.velocity == 0 ) : 
                            self.messagesFromMidiInstrument[numNotes] = { 'event': 'note_off', 'pitch': message.note, 'time': message.time, 'velocity': message.velocity }
                        else :
                            self.messagesFromMidiInstrument[numNotes] = { 'event': message.type, 'pitch': message.note, 'time': message.time, 'velocity': message.velocity }
                        numNotes += 1
                        




        except KeyboardInterrupt:
            pass

        for note in self.messagesFromMidiInstrument : 
            self.messagesFromMidiInstrument[note]['time']  = round ( self.messagesFromMidiInstrument[note]['time'] - self.initialClk , 4 ) 
            self.messagesFromMidiInstrument[note]['starttick'] =  round ( self.messagesFromMidiInstrument[note]['time'] * self.oneSecondInTicks, 0 ) 

            print ( note, self.messagesFromMidiInstrument[note] ) 

            
        #generate start and end times in ticks
        self.generateStartAndEndTimes() 

        #quantize notes
        sixteenth = 120
        eighth    = 240
        self.selfQuantizeNotes ( eighth ) 
        self.selfQuantizeNotes ( sixteenth ) 

        #remove overlaps
        self.removeOverlaps () 

        # create Midi
        self.createMidi () 

    def removeOverlaps ( self ) : 
        

        length = len(self.midiMessages) 
        overlappedIndex = [] 

        for note in self.midiMessages : 
            
            s1              = self.midiMessages[note]['starttick'] 
            actualDuration  = self.midiMessages[note]['duration']  * ( self.midiMessages[note]['velocity'] / 127.0 ) 
            e1              = self.midiMessages[note]['starttick'] + actualDuration

            for nextNote in range ( note+1, length, 1 ) : 

                s2             = self.midiMessages[nextNote]['starttick'] 
                actualDuration = self.midiMessages[nextNote]['duration']  * ( self.midiMessages[nextNote]['velocity'] / 127.0 ) 
                e2             = self.midiMessages[nextNote]['starttick'] + actualDuration
                
                
                if ( s1 <= e2 and e1 >= s2 ) : # overlap exists
                    overlappedIndex.append ( nextNote )             
                
            
        overlappedIndex = list(set( overlappedIndex ) ) 
        print() 
        print ( "Overlapped Index: ", overlappedIndex ) 

        for index in sorted(overlappedIndex, reverse=True):
            del self.midiMessages[index]

        print ( "Midi Messages after removing overlap" ) 
        
        for note in self.midiMessages : 
            print ( note, self.midiMessages[note]['pitch'],  self.midiMessages[note]['starttick'],  self.midiMessages[note]['endtick'],  self.midiMessages[note]['velocity'], 
                    self.midiMessages[note]['duration'],  self.midiMessages[note]['measure'] )
            


    def selfQuantizeNotes ( self, ticksForQuantization ) : 
        
        for note in self.midiMessages : 

            div = self.midiMessages[note]['starttick'] //  ticksForQuantization
            mod = self.midiMessages[note]['starttick'] %  ticksForQuantization

            if ( mod != 0 ) : # if note does not start on a quantized note
                if ( mod >= ticksForQuantization/2 ) : 
                    self.midiMessages[note]['starttick'] = int((div + 1 )  * ticksForQuantization )
                else : 
                    self.midiMessages[note]['starttick']      = int( div * ticksForQuantization )

                self.midiMessages[note]['endtick']            = int(self.midiMessages[note]['starttick'] + self.midiMessages[note]['duration'])
                self.midiMessages[note]['measure']            = int( self.midiMessages[note]['starttick'] / self.tsInfo['measureLength'] ) + 1
                self.midiMessages[note]['measureGranularity'] = round ( ( float(self.midiMessages[note]['starttick']) / self.tsInfo['measureLength'] ) + 1, 2 ) 

        
        print() 
        for note in self.midiMessages : 
            print ( note, self.midiMessages[note]['pitch'],  self.midiMessages[note]['starttick'],  self.midiMessages[note]['endtick'],  self.midiMessages[note]['granularity'],     
                    self.midiMessages[note]['tie'],  self.midiMessages[note]['velocity'], self.midiMessages[note]['duration'],  self.midiMessages[note]['measure'],           
                    self.midiMessages[note]['measureGranularity'],                    
                    )

            


    def createMidi ( self ) :

        # create notes from self.midiMessages
        notes = {} 
        cnt = 0 
        for note in self.midiMessages : 
            pitch     = self.midiMessages[note]['pitch']
            starttick = self.midiMessages[note]['starttick']
            endtick   = self.midiMessages[note]['endtick']
            octave    = pitch // 12
            mod       = pitch % 12
            notestr   = MusicTheory.pitchToNotes[mod]
            velocity  = self.midiMessages[note]['velocity']
            notes[cnt] = { 'event': 'on', 'notestr': notestr, 'octave': octave, 'starttick': starttick, 'velocity': velocity, 'pitch': pitch }
            cnt += 1
            notes[cnt] = { 'event': 'off', 'notestr': notestr, 'octave': octave, 'starttick': endtick, 'velocity':  0, 'pitch': pitch }
            cnt += 1


        notes = collections.OrderedDict ( sorted ( notes.items(), key=lambda x : x[1]['starttick'] )  ) 

        glbClk = 0 
        print() 
        for key in notes : 
            notes[key]['miditick'] = notes[key]['starttick'] - glbClk 
            glbClk =  notes[key]['starttick'] 
            print ( key, notes[key]['notestr'], notes[key]['event'], notes[key]['miditick'], notes[key]['pitch'] ) 


        fmt = 0
        fname   = "midi_export" 
        fnamePy = fname + ".py" 
        fout    = open ( fnamePy, "w" ) 

        fout.write ( "import midi\n" ) ;
        fout.write ( "# Instantiate a MIDI Pattern (contains a list of tracks)\n" ) ;
        fout.write ( "pattern = midi.Pattern(format=%d, resolution=%d)\n" %(fmt, self.tsInfo['resolution']) ) ;
        fout.write ( "# Instantiate a MIDI Track (contains a list of MIDI events)\n" ) ;
        fout.write ( "track = midi.Track()\n" ) ;
        fout.write ( "# Append the track to the pattern\n" ) ;
        fout.write ( "pattern.append(track)\n" ) ;
        fout.write ("# Midi Events Start Here" ) ;
        fout.write ( "\n" ) ;
        fout.write ("# Instantiate a MIDI note on event, append it to the track\n" ) ;
        fout.write ( "\n" ) ;

        tsDenominatorPow =  int(math.log ( self.tsInfo['tsDenominator'], 2 )) ;
        string = "time = midi.TimeSignatureEvent(tick=0, " + "data = [" + str(self.tsInfo['tsNumerator']) + ", " + str(tsDenominatorPow) + ", 24, 8])"  + "\n" ; # 240 bpm
        fout.write ( string ) ;
        fout.write ( "track.append(time)\n" ) 

        for i in notes : 
            
            pitch    = notes[i]['notestr'] +  "_" + str(notes[i]['octave'])
            tick     = notes[i]['miditick']
            velocity = notes[i]['velocity']
            
            if ( notes[i]['event'] == 'on' ) : 
                string = "on = midi.NoteOnEvent(tick=" + str( tick )  + ", velocity=" +  str(velocity) + ", pitch=midi." +  pitch + ")\n" 
                fout.write ( string ) ;
                fout.write ( "track.append(on)\n" ) 

            else : 

                string = "off = midi.NoteOffEvent(tick=" + str( tick ) + ", velocity=" +  str(velocity) + ", pitch=midi." +  pitch + ")\n" 
                fout.write ( string ) ;
                fout.write ( "track.append(off)\n" ) 
                

            #print ( i, pitch,  tick, velocity ) 


        fout.write ( "\n" ) ;
        fout.write ("\neot = midi.EndOfTrackEvent(tick=1)" ) ;
        fout.write ("\ntrack.append(eot)" ) ;
        fout.write ( "\n# Print out the pattern" ) ;
        fout.write ( "\n#print pattern" ) ;
        # Save the pattern to disk
    
        fout_name = fname + ".mid" ;
        fout.write ( "\nmidi.write_midifile(\"%s\", pattern)" %(fout_name) ) ;
        
        fout.close() ;

        call = "python " + fnamePy 
        print ( call ) 
        os.system ( call ) ;



    def generateStartAndEndTimes ( self ) : 


        cnt = 0 
        length = len(self.messagesFromMidiInstrument) 
        for note in self.messagesFromMidiInstrument : 
            
            if ( self.messagesFromMidiInstrument[note]['event'] == 'note_off' ) :  # ignore note off events
                continue

            for offnote in range ( note+1, length, 1 ) : 
                                
                if ( self.messagesFromMidiInstrument[offnote]['event'] == 'note_on' ) :  # ignore note on events
                    continue
                
                if (  self.messagesFromMidiInstrument[note]['pitch'] == self.messagesFromMidiInstrument[offnote]['pitch'] ) : 

                    self.midiMessages[cnt] = { 'pitch'             : self.messagesFromMidiInstrument[note]['pitch'], 
                                               'starttick'         : int(self.messagesFromMidiInstrument[note]['starttick']) ,
                                               'endtick'           : int(self.messagesFromMidiInstrument[offnote]['starttick']) , 
                                               'granularity'       : 1, 
                                               'tie'               : 0.00,
                                               'velocity'          : self.messagesFromMidiInstrument[note]['velocity'],
                                               'duration'          : int(self.messagesFromMidiInstrument[offnote]['starttick'] - self.messagesFromMidiInstrument[note]['starttick']),
                                               'measure'           : int( self.messagesFromMidiInstrument[note]['starttick'] / self.tsInfo['measureLength'] ) + 1,
                                               'measureGranularity': round ( ( float(self.messagesFromMidiInstrument[note]['starttick']) / self.tsInfo['measureLength'] ) + 1, 2 ) , 
                                               }
                    cnt += 1
                    break 



        print() 
        for note in self.midiMessages : 
            
            print ( note,
                    self.midiMessages[note]['pitch'],             
                    self.midiMessages[note]['starttick'],
                    self.midiMessages[note]['endtick'],           
                    self.midiMessages[note]['granularity'],       
                    self.midiMessages[note]['tie'],     
                    self.midiMessages[note]['velocity'],          
                    self.midiMessages[note]['duration'],          
                    self.midiMessages[note]['measure'],           
                    self.midiMessages[note]['measureGranularity'],
                    
                    )



#import djwatson_api
#from djwatson_io import Note, Const

current_milli_time = lambda: int(round(time.time() * 1000000))


class PushMidiMessages(threading.Thread):
    def __init__(self, flushIntervalInSec):
        super(PushMidiMessages, self).__init__()

        #self.queue = RecordQueue()
        self.kill_received = False
        self.flushTrigger = None
        self.flushIntervalInSec = flushIntervalInSec

    def run(self):


        for msg in inport:   # nonblocking; flush out buffered msgs and return immediately

         #   if self.flushTrigger == None and (msg.type == 'note_on' or msg.type == 'note_off'):
         #       self.flushTrigger = FlushTrigger(self.queue, self.flushIntervalInSec)
         #       self.flushTrigger.start()

#            self.queue.lock.acquire()
            #print ( msg ) 

            if msg.type == 'note_on':
#                if firstMsgTime == 0:
#                    firstMsgTime = msg.time

                #self.queue.pushNote(msg.note, convertMsgTimeToTick(msg.time), msg.velocity)
                print("note on:" ,  msg.note, "time: ", msg.time, "velocity: " , msg.velocity)

            elif msg.type == 'note_off':
                print("note off:" ,  msg.note, "time: ", msg.time, "velocity: " , msg.velocity)

                #self.queue.releaseNote(msg.note, convertMsgTimeToTick(msg.time))

#            self.queue.lock.release()
#
#            if (msg.type == 'note_on' or msg.type == 'note_off') and self.flushTrigger.trigger == True:
#                if self.flushTrigger.pendingTrigger == True:
#                    self.flushTrigger.attemptFlush()
#                else:
#                    self.flushTrigger = None



if __name__ == '__main__' :




    quarternotePerMin = 75
    ticksPerQuarterNote = 480
    msgInterval = 240 # in # of ticks
    firstMsgTime = 0 # in seconds; will be set at the first note
    flushIntervalInSec = 3.0
    
    note_min = 21
    note_max = 108
    
    
    ticksPerTie = 240
    ticksPerPush = ticksPerTie * 10
    
    firstMsgTime = 0 
    milliSecPerTick = 60000.0 / quarternotePerMin / ticksPerQuarterNote


    midi = RecordMidi() 
    midi.run() 


    sys.exit(0) 



    mido.set_backend('mido.backends.rtmidi')
    inport = mido.open_input()


    try:
        with mido.open_input() as port:
            print('Using {}'.format(port))
            print('Waiting for messages...')
            for message in port:
                print ( message.type, message.time, message.note, message.velocity ) 
                #print('Received {}'.format(message))
    except KeyboardInterrupt:
        pass

    sys.exit(0) 




    threads = []
    # pushMidi = PushMidiMessages(Const.flushIntervalInSec)
    pushMidi = PushMidiMessages(3.0)
    pushMidi.daemon = True

    threads.append(pushMidi)

    pushMidi.start()

    while True:
        try:
            pushMidi.join(1)
            # for t in threads:
            #     if t.is_alive():
            #         # print('joining thread: '+str(t))
            #         t.join(1)
        except KeyboardInterrupt:
            # for t in threads:
            #     t.kill_received = True
            break
