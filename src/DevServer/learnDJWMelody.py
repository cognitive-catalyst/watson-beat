#!/usr/bin/python


#!/usr/local/bin/python
from __future__ import print_function
import numpy as np
import time
import sys 
import re 
import os
import math
import collections
import operator
import random
import MusicTheory
#                 0     1     2     3     4     5     6     7     8     9    10    11      
PitchToNotes = [ "C", "Cs",  "D", "Ds",  "E",  "F", "Fs",  "G", "Gs",  "A", "As",  "B" ] ;
#PitchToNotes = [ "C", "C",  "D", "D",  "E",  "F", "F",  "G", "G",  "A", "A",  "B" ] ;

NotesToPitch = {
  'C' : 0,
  'Cs': 1,
  'D' : 2, 
  'Ds': 3, 
  'E' : 4, 
  'F' : 5, 
  'Fs': 6, 
  'G' : 7, 
  'Gs': 8, 
  'A' : 9, 
  'As': 10,
  'B' : 11 } ;
  

pitchToNotes = {
  0 :'C'  ,
  1 :'Cs' ,
  2 :'D'  , 
  3 :'Ds' , 
  4 :'E'  , 
  5 :'F'  , 
  6 :'Fs' , 
  7 :'G'  , 
  8 :'Gs' , 
  9 :'A'  , 
  10:'As' ,
  11:'B'  , } ;
                                  


def _min ( a , b ) :
  if ( a < b ) :
    return a ;
  else :
    return b ;




def WriteInitialMidiFileSequence ( fout ) : 
    
  fout.write ( "import midi\n" ) ;
  fout.write ( "# Instantiate a MIDI Pattern (contains a list of tracks)\n" ) ;
  fout.write ( "pattern = midi.Pattern(format=%d, resolution=%d)\n" %(0, 480) ) ; #tsInfo['resolution']) ) ;
  fout.write ( "# Instantiate a MIDI Track (contains a list of MIDI events)\n" ) ;
  fout.write ( "track = midi.Track()\n" ) ;
  fout.write ( "# Append the track to the pattern\n" ) ;
  fout.write ( "pattern.append(track)\n" ) ;
  fout.write ("# Midi Events Start Here" ) ;
  fout.write ( "\n" ) ;
  fout.write ("# Instantiate a MIDI note on event, append it to the track\n" ) ;
  fout.write ( "\n" ) ;

def WriteMidiEvents ( fout, data ) : 
  for cnt in data  : 
    item = data[cnt] 
    #print ( item ) 
    if ( item['event'] == 'on' ) : 
      string = "on = midi.NoteOnEvent(tick=" + str( item['midiClk'] ) + ", velocity=" +  str(item['velocity']) + ", pitch=" + item['pitch']  + ")" + "\n" ;
      fout.write ( string ) ;
      fout.write ( "track.append(on)\n" ) 
    elif ( item['event'] == 'off' ) : 
      string = "off = midi.NoteOffEvent(tick=" + str( item['midiClk'] ) + ", velocity=" +  str(item['velocity']) + ", pitch=" + item['pitch']  + ")" + "\n" ;
      fout.write ( string ) ;
      fout.write ( "track.append(off)\n" ) 
    elif ( item['event'] == 'tse' ) :                     
      string = "time = midi.TimeSignatureEvent(tick=" + str( item['midiClk'] ) +  ", data = " + item['data'] + ")" + "\n" ; 
      fout.write ( string ) ;
      fout.write ( "track.append(time)\n" ) 
    elif ( item['event'] == 'tempo' ) :                     
      string = "tempo = midi.SetTempoEvent(tick=" + str( item['midiClk'] ) +  ", data = " + item['data'] + ")" + "\n" ; 
      fout.write ( string ) ;
      fout.write ( "track.append(tempo)\n" )                 
    elif ( item['event'] == 'comment' ) :                     
      string = item['data'] + "\n" 
      fout.write ( string ) ;
      

def WriteFinalMidiFileSequence (  fout, foutName ) :
    
  foutMidiName = foutName + ".mid" 
  fout.write ( "\n" ) ;
  fout.write ("# Midi Events End Here" ) ;
  fout.write ("\neot = midi.EndOfTrackEvent(tick=1)" ) ;
  fout.write ("\ntrack.append(eot)" ) ;
  fout.write ( "\n# Print out the pattern" ) ;
  fout.write ( "\n#print pattern" ) ;
  # Save the pattern to disk
  fout.write ( "\nmidi.write_midifile(\"%s\", pattern)" %(foutMidiName) ) ;
  fout.close() ;
            
  # print ( "\nOutput midi file: %s\n" %(foutMidiName) ) ;
  call = "python " + foutName + ".py"  ; 
  os.system ( call ) ;



class RBM:
  
  def __init__(self, num_visible, num_hidden, learning_rate = 0.1):
    self.num_hidden = num_hidden
    self.num_visible = num_visible
    self.learning_rate = learning_rate

    # Initialize a weight matrix, of dimensions (num_visible x num_hidden), using
    # a Gaussian distribution with mean 0 and standard deviation 0.1.
    self.weights = 0.1 * np.random.randn(self.num_visible, self.num_hidden)    
    # Insert weights for the bias units into the first row and first column.
    
    self.weights = np.insert(self.weights, 0, 0, axis = 0)
    

    #print ( "Weights" ) ;
    self.weights = np.insert(self.weights, 0, 0, axis = 1)
    #print ( self.weights) ;


  def train(self, data, max_epochs = 1000, start_epoch = 1 ):
    """
    Train the machine.

    Parameters
    ----------
    data: A matrix where each row is a training example consisting of the states of visible units.    
    """
    if ( start_epoch == 1 ) : 
      self.weights = 0.1 * np.random.randn(self.num_visible, self.num_hidden)    
      # Insert weights for the bias units into the first row and first column.
      self.weights = np.insert(self.weights, 0, 0, axis = 0)
      #print ( "Weights" ) ;
      self.weights = np.insert(self.weights, 0, 0, axis = 1)
      #print ( self.weights) ;

    

    num_examples = data.shape[0]
    # Insert bias units of 1 into the first column.
    data = np.insert(data, 0, 1, axis = 1)

    #print ( "\nData" ) ;
    #print ( data) ;


    for epoch in range(start_epoch, max_epochs):      

      # Clamp to the data and sample from the hidden units. 
      # (This is the "positive CD phase", aka the reality phase.)
      pos_hidden_activations = np.dot(data, self.weights)      
      #print ("\npos_hidden_activations" ) ;
      #print ( pos_hidden_activations )
      #print ("\npos_hidden_probabilities after sigmoid logistic function" ) ;
      pos_hidden_probs = self._logistic(pos_hidden_activations)
      #print ( pos_hidden_probs ) 


      #print ( "\nPositive hidden states" )
      pos_hidden_states = pos_hidden_probs > np.random.rand(num_examples, self.num_hidden + 1)
      #print ( pos_hidden_states) 
     

      # Note that we're using the activation *probabilities* of the hidden states, not the hidden states       
      # themselves, when computing associations. We could also use the states; see section 3 of Hinton's 
      # "A Practical Guide to Training Restricted Boltzmann Machines" for more.

      pos_associations = np.dot(data.T, pos_hidden_probs)
      #print ( "\npos_associations") ;
      #print ( pos_associations) 


      # Reconstruct the visible units and sample again from the hidden units.
      # (This is the "negative CD phase", aka the daydreaming phase.)
      #print ("\nnegative_visible_activations" ) ;
      #neg_visible_activations = np.dot(pos_hidden_states, self.weights.T)

      #pos_hidden_probs[:,1] = 0.67
      

      neg_visible_activations = np.dot(pos_hidden_probs, self.weights.T)


      #print ( neg_visible_activations ) ;
      #print ("\nneg_visible_probabilities after sigmoid logistic function" ) ;
      neg_visible_probs = self._logistic(neg_visible_activations)
      #print ( neg_visible_probs ) ;

      neg_visible_probs[:,0] = 1 # Fix the bias unit.
      #if ( self.num_visible > 300 ) :
      #neg_visible_probs[:,1] = 0.67 # Fix the bias unit.

      #print ("\nneg_visible_probabilities after fixing bias unit" ) ;
      #print ( neg_visible_probs ) ;


      #print ( "\nneg_hidden_activation" ) ;
      neg_hidden_activations = np.dot(neg_visible_probs, self.weights)
      #print ( neg_hidden_activations) ;
      #print ( "\nneg_hidden_probs" ) ;
      neg_hidden_probs = self._logistic(neg_hidden_activations)
      #print ( neg_hidden_probs) ;
      # Note, again, that we're using the activation *probabilities* when computing associations, not the states 
      # themselves.
      neg_associations = np.dot(neg_visible_probs.T, neg_hidden_probs)
      #print ( "\nneg_associations") ;
      #print ( neg_associations) 

      # Update weights.
      self.weights += self.learning_rate * ((pos_associations - neg_associations) / num_examples)

      error = np.sum((data - neg_visible_probs) ** 2)
      if ( epoch % 1000 == 0 ) : 
        print("Epoch %s: error is %s" % (epoch, error))

    return neg_hidden_probs ;


  def run_visible(self, data):
    """
    Assuming the RBM has been trained (so that weights for the network have been learned),
    run the network on a set of visible units, to get a sample of the hidden units.
    
    Parameters
    ----------
    data: A matrix where each row consists of the states of the visible units.
    
    Returns
    -------
    hidden_states: A matrix where each row consists of the hidden units activated from the visible
    units in the data matrix passed in.
    """
    
    num_examples = data.shape[0]
    
    # Create a matrix, where each row is to be the hidden units (plus a bias unit)
    # sampled from a training example.
    hidden_states = np.ones((num_examples, self.num_hidden + 1))
    
    # Insert bias units of 1 into the first column of data.
    data = np.insert(data, 0, 1, axis = 1)

    # Calculate the activations of the hidden units.
    hidden_activations = np.dot(data, self.weights)
    # Calculate the probabilities of turning the hidden units on.
    hidden_probs = self._logistic(hidden_activations)
    # Turn the hidden units on with their specified probabilities.
    #hidden_states[:,:] = hidden_probs > np.random.rand(num_examples, self.num_hidden + 1)
    hidden_states[:,:] = hidden_probs ; 
    # Always fix the bias unit to 1.
    # hidden_states[:,0] = 1
  
    # Ignore the bias units.
    hidden_states = hidden_states[:,1:]
    return hidden_states
    
  # TODO: Remove the code duplication between this method and `run_visible`?
  def run_hidden(self, data):
    """
    Assuming the RBM has been trained (so that weights for the network have been learned),
    run the network on a set of hidden units, to get a sample of the visible units.

    Parameters
    ----------
    data: A matrix where each row consists of the states of the hidden units.

    Returns
    -------
    visible_states: A matrix where each row consists of the visible units activated from the hidden
    units in the data matrix passed in.
    """

    num_examples = data.shape[0]

    #print (num_examples) ;

    # Create a matrix, where each row is to be the visible units (plus a bias unit)
    # sampled from a training example.
    visible_states = np.ones((num_examples, self.num_visible + 1))

    #print (visible_states.shape);

    # Insert bias units of 1 into the first column of data.
    #data = np.insert(data, 0, 1, axis = 1)

    data[:,0] = 1 ;

    #print (data.shape) ;
    #print (self.weights.shape)

    # Calculate the activations of the visible units.
    visible_activations = np.dot(data, self.weights.T)
    # Calculate the probabilities of turning the visible units on.
    visible_probs = self._logistic(visible_activations)
    # Turn the visible units on with their specified probabilities.
    #visible_states[:,:] = visible_probs > np.random.rand(num_examples, self.num_visible + 1)
    visible_states[:,:] = visible_probs ; 
    # Always fix the bias unit to 1.
    # visible_states[:,0] = 1

    # Ignore the bias units.
    visible_states = visible_states[:,1:]
    return visible_states
    
  def daydream(self, num_samples):
    """
    Randomly initialize the visible units once, and start running alternating Gibbs sampling steps
    (where each step consists of updating all the hidden units, and then updating all of the visible units),
    taking a sample of the visible units at each step.
    Note that we only initialize the network *once*, so these samples are correlated.

    Returns
    -------
    samples: A matrix, where each row is a sample of the visible units produced while the network was
    daydreaming.
    """

    # Create a matrix, where each row is to be a sample of of the visible units 
    # (with an extra bias unit), initialized to all ones.
    samples = np.ones((num_samples, self.num_visible + 1))

    # Take the first sample from a uniform distribution.
    samples[0,1:] = np.random.rand(self.num_visible)

    # Start the alternating Gibbs sampling.
    # Note that we keep the hidden units binary states, but leave the
    # visible units as real probabilities. See section 3 of Hinton's
    # "A Practical Guide to Training Restricted Boltzmann Machines"
    # for more on why.
    for i in range(1, num_samples):
      visible = samples[i-1,:]

      # Calculate the activations of the hidden units.
      hidden_activations = np.dot(visible, self.weights)      
      # Calculate the probabilities of turning the hidden units on.
      hidden_probs = self._logistic(hidden_activations)
      # Turn the hidden units on with their specified probabilities.
      hidden_states = hidden_probs > np.random.rand(self.num_hidden + 1)
      # Always fix the bias unit to 1.
      hidden_states[0] = 1

      # Recalculate the probabilities that the visible units are on.
      visible_activations = np.dot(hidden_states, self.weights.T)
      visible_probs = self._logistic(visible_activations)
      visible_states = visible_probs > np.random.rand(self.num_visible + 1)
      samples[i,:] = visible_states

    # Ignore the bias units (the first column), since they're always set to 1.
    return samples[:,1:]        
      
  def _logistic(self, x):
    return 1.0 / (1 + np.exp(-x))


def run ( training_pitch, training_starttime, training_endtime, Scale ) :
  
  #np.random.seed( 20 ) ;

  creativity_genes = 2

  if ( 0 ) :
    print ( "Creativity Genes: " , creativity_genes )
    print ( "Training Pitch: " , training_pitch ) ; 
    print ( "Training start Time: " , training_starttime ) 
    print ( "Training end Time: " , training_endtime ) 
    print()



  # TO DO 1: WHEN WE FIX THE CHORD ISSUE, THIS VALUE WILL COME FROM ./MeasureBasedPartitionDumpFile, WHICH WILL FIGURE OUT THE OVERLAPS BASED ON START AND END TIME OF EACH NOTE THAT IS BEING PLAYED
  num_note_slices = 1 # because this will be a single note melody 
  num_time_slices = len(training_pitch) ; 
  
  # ABSOLUTELY WE WILL TRAIN RHYTHM AND PITCH. So add tie note for each pitch neuron being played
  num_note_slices += 1 

  # account for tie notes for the creativity genes.
  creativity_genes = creativity_genes * 2 

  # add creativity genes to the actual pitch neurons
  num_note_slices += creativity_genes ;

  if ( 0 ) : 

    print ( "\nAddtional Creativity Genes (and corresponding tie notes) added is: %d" %(creativity_genes)) 
    print ( "\nActual Note Slices After adjusting for rhythmn and Creativity Gene is: %d" %(num_note_slices) ) 
    print ( "\nNumber of time slices: %d" %(num_time_slices)) ;

  #sys.exit(0) 



  start = [ 1 ]
  end   = [ 1000 ]


  training_data = [ 0 for i in range( ( num_note_slices + 0 ) * ( num_time_slices  ) ) ] ;
  total_neurons = num_note_slices * num_time_slices ;

  cnt = 0 ;  

  lengthOfScale = len(Scale) 
  if ( Scale[lengthOfScale-3] == 'n' ) : 
    scaleHashTerm = 'Minor'
    pentatonic_notes = [1,3,4,5,7] 
  elif ( Scale[lengthOfScale-3] == 'j' ) : 
    scaleHashTerm = 'Major'
    pentatonic_notes = [1,2,3,5,6] 
  elif ( Scale[lengthOfScale-1] == 't' ) : 
    scaleHashTerm = 'Oct'
    pentatonic_notes = [1,2,3,4,5,6,7,8] 
  elif ( Scale[lengthOfScale-1] == 'c' ) : 
    scaleHashTerm = 'CArabic'
    pentatonic_notes = [1,2,3,4,5,6,7] 

  #print ( Scale, scaleHashTerm ) 
  #pentatonic_notes = MusicTheory.Pentatonic[scaleHashTerm] 
  # to bias randomnly instead of using pentatonic use all seven notes of the scale
  # pentatonic_notes = [1, 2, 3, 4, 5, 6, 7] 


  #print ( "pentatonic notes: " , pentatonic_notes) ;
  # randomly remove one or two notes from the pentatonic scale to make it less oriental
  random.shuffle(pentatonic_notes) 
  #print ( "pentatonic notes after shuffling: " , pentatonic_notes) ;
  pentatonic_notes.pop()
  #print ( "pentatonic notes after popping: " , pentatonic_notes) ;
  if ( random.randint(1,10) > 8 ) : # pop one more elemnt 20% of the time
    random.shuffle(pentatonic_notes) 
    #print ( "pentatonic notes after shuffling: " , pentatonic_notes) ;
    pentatonic_notes.pop()
    #print ( "pentatonic notes after popping: " , pentatonic_notes) ;


  for i in range( num_time_slices ) :
    octave = 0 
    biasToTieNeuron = False 
    for j in range ( 0, num_note_slices, 2 ) : 
      if ( j == 0 ) :
        training_data[cnt]   = training_pitch[i] 
        training_data[cnt+1] = 0.0
        octave = (training_pitch[i] * 100 ) // 12
        cnt += 1
      else : 

        pentatonic_index = random.choice(pentatonic_notes)  # choose a random penatatonic pitch 
        newNote = MusicTheory.ReverseKeyDict[Scale][pentatonic_index] 
        training_data[cnt] = float (  ( octave * 12 ) + MusicTheory.NotesToPitch[newNote] ) / 100 
        
        if ( biasToTieNeuron ) :
          training_data[cnt+1] = random.choice( [ 0.00, 0.15, 0.0, 0.15, 0.15 ] )  # choose tie note 60% of the time        
        else : 
          training_data[cnt+1] = random.choice( [ 0.00, 0.15 ] ) # choose a random tie note
        cnt += 1
      cnt += 1 ;
          
  if ( 0 ) :
    for i in range( num_time_slices ) :
      val = [] 
      for j in range ( num_note_slices ) : 
        val.append( training_data[i*num_note_slices + j ]) 
      print ( i, val )
    print ( "\n" ) ;
      

  for k in range(1) :

    # Initialize the RBM layers for the DBN. Also set the number of times we want to train the files
    r1 = RBM(num_visible = len(training_data), num_hidden = len(training_data)/2)
    r2 = RBM ( num_visible = len(training_data) / 2 + 1, num_hidden = len(training_data) / 4 ) 
    r3 = RBM ( num_visible = len(training_data) / 4 + 1, num_hidden = len(training_data) / 8 )  
  
  
    flag = 0 ;

    for iter in range ( len (start) ) : 

      training_data_r1 = np.array ( [training_data] ) ;

      neg_hidden_probs =  r1.train(training_data_r1, max_epochs = end[iter], start_epoch = start[iter] )     
      training_data_r2 = neg_hidden_probs ;
      neg_hidden_probs = r2.train (training_data_r2, max_epochs = end[iter], start_epoch = 1 ) 
  
  
      training_data_r3 = neg_hidden_probs ;
      neg_hidden_probs = r3.train (training_data_r3, max_epochs = end[iter], start_epoch = 1 ) 
  
      output =  r3.run_hidden ( neg_hidden_probs )  ;
      output =  r2.run_hidden ( output )  ;
      output =  r1.run_hidden ( output )  ;
  
      #print ( "len of output: ", len(output[0]) ) 

      #output[0] =   ( output[0] * 1000 ) ;
      output[0] =   ( output[0] * 100 ) ;
      selected_output = [] 
      selected_notes = [] 
      selected_ties = [] 

      #print ( "Output: ", output[0] ) 

      # Make sure note falls within scale
      for i in range( num_time_slices ) :
        notes = [] 
        ties = [] 
        for j in range ( 0, num_note_slices, 2 ) : 
          
          #output[0][i*num_note_slices + j ] = output[0][i*num_note_slices + j ]//10 
          output[0][i*num_note_slices + j] = round ( output[0][i*num_note_slices + j], 0 )  

          note = '' 
          note = MusicTheory.pitchToNotes[output[0][i*num_note_slices + j] % 12] 

          notes.append(  output[0][i*num_note_slices + j ] ) 

          output[0][i*num_note_slices + j+1 ] = round ( output[0][i*num_note_slices + j+1 ], 2 ) 
          if ( output[0][i*num_note_slices + j+1 ] > 10 ) : 
            output[0][i*num_note_slices + j+1 ] = 15 # make it a tie note
          else :
            output[0][i*num_note_slices + j+1 ] = 0 # dont make it a tie note

          ties.append( output[0][i*num_note_slices + j+1 ] )                 

        selected_output.append( int(collections.Counter (notes).most_common(1)[0][0] ) )
        selected_notes.append ( MusicTheory.pitchToNotes[collections.Counter (notes).most_common(1)[0][0] % 12 ] ) 
        selected_ties.append( int(collections.Counter (ties).most_common(1)[0][0] ) )

        #print ( i, notes, collections.Counter (notes).most_common(1)[0][0] , ties, collections.Counter (ties).most_common(1)[0][0]   )
        
      #print ( "\n" ) ;
      pentatonic = False 
      withinScale = True
      numTimes = 0 
      new_output = []
      initial = True
      for note in selected_output :
        if ( initial ) : 
          initial = False 
          noteStr = MusicTheory.pitchToNotes[note % 12] 
          if ( noteStr not in MusicTheory.AllChords[Scale] ) : 
            noteStr = random.choice(MusicTheory.AllChords[Scale]) 
            octave = note // 12
            noteStrIndex = MusicTheory.NotesToPitch[noteStr] 
            note = ( octave * 12 ) + noteStrIndex 
            

        if ( pentatonic ) :
          noteStr = MusicTheory.pitchToNotes[note % 12] 
          while ( noteStr not in MusicTheory.PentatonicScale[Scale] ) :
            noteA = note + 1
            noteB = note - 1
            if ( random.randint ( 0, 100 ) > 50 ) : 
              noteStr = MusicTheory.pitchToNotes[noteA % 12] 
              note = noteA
            else :
              noteStr = MusicTheory.pitchToNotes[noteB % 12] 
              note = noteB
        elif ( withinScale ) : 
          noteStr = MusicTheory.pitchToNotes[note % 12] 

          if ( noteStr not in MusicTheory.KeyDict[Scale] ) :
            noteStrA = noteStr
            noteStrB = noteStr

            while ( noteStrA not in MusicTheory.KeyDict[Scale] ) :
              noteA = note + 1
              noteStrA = MusicTheory.pitchToNotes[noteA % 12] 

            while ( noteStrB not in MusicTheory.KeyDict[Scale] ) :
              noteB = note + 1
              noteStrB = MusicTheory.pitchToNotes[noteB % 12] 
              
            if ( abs(note-noteA) < abs(note-noteB) ) :
              note = noteA
            else :
              note = noteB


        new_output.append ( note ) 
        
      #selected_output  = [ i/ 100.0 for i in selected_output ]
      #print ( selected_output )
      #print ( new_output )

  training_pitch = [ int(i * 100) for i in training_pitch ] 
  #print ( training_pitch ) ; 
  #print ( new_output ) 

  return ( new_output ) 

  

  
def createMidi ( pitch, startTime, endTime, foutName ) : 
  
  glbClk = 0 
  events = collections.OrderedDict()
  cnt = 0 
  print ( pitch ) 
  for i in range(len(pitch)) :
    note = pitch[i]
    noteStr = MusicTheory.pitchToNotes[note%12]
    octave = note // 12
    duration =  endTime[i] - startTime[i]

    clk = startTime[i] - glbClk

    events[cnt] = { 'event': 'on', 'midiClk': clk, 'note': note, 'pitch': "midi." + noteStr + "_" + str(octave), 'octave': octave, 'velocity': random.randint(50, 80) } 
    cnt += 1
    events[cnt] = { 'event': 'off', 'midiClk': duration, 'note': note, 'pitch': "midi." + noteStr + "_" + str(octave), 'octave': octave, 'velocity': 0 }
    cnt += 1

    glbClk = endTime[i]


  # create final MIDI File
  fout = open ( foutName+".py", mode='w' ) ;
  print ( "foutName ", foutName+ ".py" ) ;

  WriteInitialMidiFileSequence ( fout ) 
  WriteMidiEvents ( fout, events ) 
  WriteFinalMidiFileSequence ( fout, foutName ) 


if __name__ == '__main__':

  training_pitch = [0.40, 0.38, 0.36, 0.38, 0.40, 0.40, 0.40, 0.38, 0.38, 0.38, 0.40, 0.43, 0.43 ]
  training_starttime = [ 0,480,960,1440,1920,2400,2880,3840,4320,4800,5760,6240,6720]
  training_endtime = [433,913,1393,1873,2353,2833,3746,4273,4753,5666,6193,6673,7586 ]
  Scale = 'CMajor'

  trainedPitches = run ( training_pitch, training_starttime, training_endtime, Scale )

  training_pitch = [ int(i * 100) for i in training_pitch ] 
  createMidi ( training_pitch, training_starttime, training_endtime, "oldFile" ) 
  createMidi ( trainedPitches, training_starttime, training_endtime, "newFile" ) 
