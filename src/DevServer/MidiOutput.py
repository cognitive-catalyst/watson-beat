from __future__ import print_function
import os
import sys
import math
import time
import random 
import collections

import MusicTheory

def createOutputMidiFileOctaveBalanced ( data, trIter, foutName, tsInfo, baseOctave ) : 
    print () 
    print ( "Creating Output Midi file for Iteration Number: ", trIter ) 

    #octave = 4
    octaveBalancedData = {} 
    restClk = 0 

    foutMidiName = foutName + "_" + str(trIter) + "_train.mid" 
    #foutName = foutName + "_" + str(trIter) + "_train.py" 

    foutMidiName = foutName + "_" + str(trIter) + ".mid" 
    foutName = foutName + "_" + str(trIter) + ".py" 

    # create final MIDI File
    fout = open ( foutName, mode='w' ) ;
    print ( "foutName ", foutName ) ;

    WriteInitialMidiFileSequence ( fout, tsInfo ) 

    prevNote = ''
    octave   = baseOctave 

    for item in data : 

        for note in range(len(item['notes'])) :

            if ( item['notes'][note] != 'Rest' ) : 
                startTick = restClk 
                endTick = item['duration'][note] 

                if ( 'octaveUp' in item ) :  # for Bass2 only
                    if ( item['octaveUp'] ) : 
                        octave = baseOctave + 1
                    else : 
                        octave = baseOctave 
                elif ( 'pitches' in item and (len(item['pitches']) > 0 ) )   :                     
                    octave = item['pitches'][note] // 12 
                else :                     
                    currNoteIndex = MusicTheory.NotesToPitch[item['notes'][note]]
                    if ( prevNote != '' ) : 
                        if ( prevNoteIndex - currNoteIndex >= 7 ) : 
                            octave += 1
                        elif ( prevNoteIndex - currNoteIndex <= -7 ) : 
                            octave -= 1

                prevNote = item['notes'][note]
                prevNoteIndex = MusicTheory.NotesToPitch[prevNote] 


                velocity = random.randint ( 50, 85 ) 
                string = "on = midi.NoteOnEvent(tick=" + str( startTick ) + ", velocity=" +  str(velocity) + ", pitch=midi." +  item['notes'][note] + "_" + str(octave)  + ")" + "\n" ;
                fout.write ( string ) ;
                fout.write ( "track.append(on)\n" ) 
                string = "off = midi.NoteOffEvent(tick=" + str( endTick ) + ", velocity=" +  str(0) + ", pitch=midi." +  item['notes'][note] + "_" + str(octave)  + ")" + "\n" ;
                fout.write ( string ) ;
                fout.write ( "track.append(off)\n" ) 

                restClk = 0 
            else : 
                restClk += item['duration'][note] 
                
    fout.write ( "\n" ) ;
    fout.write ("# Midi Events End Here" ) ;
    fout.write ("\neot = midi.EndOfTrackEvent(tick=1)" ) ;
    fout.write ("\ntrack.append(eot)" ) ;
    fout.write ( "\n# Print out the pattern" ) ;
    fout.write ( "\n#print pattern" ) ;
    # Save the pattern to disk
    fout.write ( "\nmidi.write_midifile(\"%s\", pattern)" %(foutMidiName) ) ;
    fout.close() ;
        
    print ( "\nOutput midi file: %s\n" %(foutMidiName) ) ;
    call = "python " + foutName ; 
    os.system ( call ) ;
        





def WriteInitialMidiFileSequence ( fout, tsInfo ) : 

  fout.write ( "import midi\n" ) ;
  fout.write ( "# Instantiate a MIDI Pattern (contains a list of tracks)\n" ) ;
  fout.write ( "pattern = midi.Pattern(format=%d, resolution=%d)\n" %(0, tsInfo['resolution']) ) ;
  fout.write ( "# Instantiate a MIDI Track (contains a list of MIDI events)\n" ) ;
  fout.write ( "track = midi.Track()\n" ) ;
  fout.write ( "# Append the track to the pattern\n" ) ;
  fout.write ( "pattern.append(track)\n" ) ;
  fout.write ("# Midi Events Start Here" ) ;
  fout.write ( "\n" ) ;
  fout.write ("# Instantiate a MIDI note on event, append it to the track\n" ) ;
  fout.write ( "\n" ) ;


  tsDenominatorPow =  int(math.log ( tsInfo['tsDenominator'], 2 )) ;
  string = "time = midi.TimeSignatureEvent(tick=0, " + "data = [" + str(tsInfo['tsNumerator']) + ", " + str(tsDenominatorPow) + ", 24, 8])"  + "\n" ; # 240 bpm
  fout.write ( string ) ;
  fout.write ( "track.append(time)\n" ) 


  #string = "tempo = midi.SetTempoEvent(tick=0, " + "data = (15, 66, 64 ))"  + "\n" ;  # 60 bpm
  #string = "tempo = midi.SetTempoEvent(tick=0, " + "data = (07, 161, 32 ))"  + "\n" ; # 120 bpm
  #string = "tempo = midi.SetTempoEvent(tick=0, " + "data = (03, 208, 144 ))"  + "\n" ; # 240 bpm
  #fout.write ( string ) ;
  #fout.write ( "track.append(tempo)\n" ) 

  fout.write ( "cce = midi.ControlChangeEvent(tick=0, data = [0, 0])" + "\n" ) ; 
  fout.write ( "track.append(cce)"  + "\n"  ) ; 

