from __future__ import print_function
import sys
import copy
import random
import collections
import DrumConstants
from Skeleton import Constants



class DrumFill: 

    '''
    # movement indicates the movement of the sticks on the different pieces of the drumkit
    # High indicates that the drummer starts from the pieces stacked up hight -> like the cymbals -> crash, ride, hihat closed, open foot
    # mid indicates the pieces in the middle -> hi Tom, mid Tom and Snare
    # low indicares the pieces near the foor of the drummer -> floor Tom, Kick Drum
    '''
    def __init__ ( self, tse, startBeat, numBeats, rhythmSpeed, complexity ) : 

        #rhythmSpeed = 'slow'
        #complexity = 'super-simple'
        #rhythmSpeed = 'medium'


        if ( complexity.endswith ( 'simple' ) ) : 
            maxMovementPoints = random.choice ( [ 1, 2, 2, 3 ] )   # this is indicates the number of  movements of the drumsticks , eg: high mid low high            
            maxMovementPoints = random.choice ( [ 1, 2, 2, 2 ] )   # this is indicates the number of  movements of the drumsticks , eg: high mid low high            
            self.maxParallel = 2 # how many notes can play at the same time
        else : 
            maxMovementPoints = random.choice ( [ 2, 3, 3 ] )   # this is indicates the number of  movements of the drumsticks , eg: high mid low high
            self.maxParallel = 2 # how many notes can play at the same time


        movementTypes = ['high', 'mid', 'low' ] 


        
        # pick number of beats for first gesture position based on rand ( maxbeats/2 to maxbeats/4 ) 
        numBeatsForGesturePosition = []
        numBeatsForPosition = max ( 1, random.randint ( numBeats//4, numBeats//2 ) ) 
        remainingBeats = numBeats - numBeatsForPosition
        numBeatsForGesturePosition.append ( numBeatsForPosition ) 
        for i in range(1, maxMovementPoints)  : 
            if ( i == maxMovementPoints-1 ) : # if this is the last gesture position, assign remaining beats to this position
                numBeatsForGesturePosition.append ( remainingBeats ) 
            else : # else assign remainingBeats // 2 for this position
                numBeatsForPosition = max ( 1, remainingBeats//2 ) 
                remainingBeats -= numBeatsForPosition
                numBeatsForGesturePosition.append ( numBeatsForPosition ) 
                
        # shuffle the list to add randomness
        random.shuffle(numBeatsForGesturePosition)

        self.gesturePosition = []
        for i in range( maxMovementPoints)  : 

            if ( rhythmSpeed == 'slow') : 
                maxDensity = max ( 1, random.randint ( numBeatsForGesturePosition[i]//4,  numBeatsForGesturePosition[i]//2 ) )   # how crowded should the fill be
            elif ( rhythmSpeed == 'medium') : 
                maxDensity = max ( 1, random.randint ( numBeatsForGesturePosition[i]//2,  (3* numBeatsForGesturePosition[i]) // 4 ) )  # how crowded should the fill be
            elif ( rhythmSpeed == 'fast') : 
                maxDensity = (3*numBeatsForGesturePosition[i]) // 4  # how crowded should the fill be 
            
            fillBeats = {}
            for j in range(maxDensity) : 
                num = random.randint( 1, numBeatsForGesturePosition[i] ) 
                while num in fillBeats : 
                    num = random.randint( 1, numBeatsForGesturePosition[i] ) 
                fillBeats[num] = True
            

            self.gesturePosition.append ( { 'position': random.choice ( movementTypes ), 'numBeats': numBeatsForGesturePosition[i], 'maxDensityInBeats': maxDensity, 'fillBeats': fillBeats } ) 
            
            
        self.numBeats = numBeats # for 4/4, end of section fill the max beats is from 8 to 16. 1/2 a measure to 1 measure. for
        self.startFillBeat = startBeat

        if ( 0 ) : 
            print ( "Tse: ", tse, "StartBeat: ", self.startFillBeat, "NumBeats: ", self.numBeats, "Complexity: ", complexity, "RhythmSpeed: ", rhythmSpeed, "MaxMovementPoints: ", maxMovementPoints, numBeatsForGesturePosition ) 
            for i in range( maxMovementPoints)  : 
                print ( self.gesturePosition[i] ) 





    def createFills ( self ) : 
        minCrashOrRideDistance = 4  # min beats bewteen a crash/ride and another crash/ride
        lastCrashOrRideBeat = -4 # indeicates beat for the most recent crash or ride. will be used for making sure minCrashRideDistance is maintained
        
        currBeatNum = self.startFillBeat        
        fillMeasure = collections.OrderedDict() 

        cnt = 0 

        if ( currBeatNum != 1 ) : 
            # rest note
            fillMeasure[cnt] = { 'beatNum': 1, 'event': 'on',  'note':DrumConstants.fillNotes['low']['kick'],'velocity': 0,'midiClk': 0, 'octave': DrumConstants.fillNoteOctaves['low']['kick'], 'pitch': "midi." + DrumConstants.fillNotes['low']['kick'] + "_" + str(DrumConstants.fillNoteOctaves['low']['kick']) } 
            fillMeasure[cnt+1] = { 'beatNum': 1, 'event': 'off', 'note':DrumConstants.fillNotes['low']['kick'],'velocity': 0,'midiClk': (currBeatNum-1)*DrumConstants.SmallestGranularityInTicks, 'octave':DrumConstants.fillNoteOctaves['low']['kick'], 'pitch':"midi."+DrumConstants.fillNotes['low']['kick']+"_"+str(DrumConstants.fillNoteOctaves['low']['kick']) } 
            cnt += 2

        
        for gesturePos in self.gesturePosition : 

            position = gesturePos['position'] 

            for beat in range(1,  gesturePos['numBeats']+1) : 
                                
                if ( beat in gesturePos['fillBeats'] ) : 


                    notesInCurrBeat = random.randint ( 1, self.maxParallel ) 
                    inst = [] 
                    notes = []
                    octaves = []
                    velocity = []
                    for i in range(notesInCurrBeat) :
                        
                        instrument = random.choice ( DrumConstants.fillPieces[position] )                         

                        if ( instrument == 'crash' or instrument == 'ride' ) : 
                            crDist = currBeatNum - lastCrashOrRideBeat 
                        else :
                            crDist = minCrashOrRideDistance

                        while ( instrument in inst or crDist < minCrashOrRideDistance )  : 
                            instrument = random.choice ( DrumConstants.fillPieces[position] ) 
                            if ( instrument == 'crash' or instrument == 'ride' ) : 
                                crDist = currBeatNum - lastCrashOrRideBeat 
                            else :
                                crDist = minCrashOrRideDistance


                        inst.append ( instrument ) 
                        if ( instrument == 'crash' or instrument == 'ride' ) : 
                            lastCrashOrRideBeat = currBeatNum

                        notes.append ( DrumConstants.fillNotes[position][instrument] ) 
                        octaves.append ( DrumConstants.fillNoteOctaves[position][instrument] ) 
                        velocity.append ( random.randint ( 60, 120 ) ) 

                    for i in range(len(notes)) : 

                        fillMeasure[cnt]   = { 'beatNum': currBeatNum, 'event': 'on',  'note':notes[i], 'velocity': velocity[i], 'midiClk': 0, 'octaves': octaves[i], 'pitch': "midi." + notes[i] + "_" + str(octaves[i]) } 
                        cnt += 1
                        
                    fillMeasure[cnt] = { 'beatNum': currBeatNum, 'event': 'off', 'note':notes[0], 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octaves': octaves[0], 'pitch': "midi." + notes[0] + "_" + str(octaves[0]) } 
                    cnt += 1
                    for i in range(1, len(notes)) : 

                        fillMeasure[cnt] = { 'beatNum': currBeatNum, 'event': 'off', 'note':notes[i], 'velocity': 0, 'midiClk': 0, 'octaves': octaves[i], 'pitch': "midi." + notes[i] + "_" + str(octaves[i]) } 
                        cnt += 1


                else :  # rest note
                    fillMeasure[cnt]   = { 'beatNum': currBeatNum, 'event': 'on',  'note':'C', 'velocity': 0, 'midiClk': 0, 'octaves': 3, 'pitch': "midi.C_3"  } 
                    cnt += 1
                    fillMeasure[cnt]   = { 'beatNum': currBeatNum, 'event': 'off',  'note':'C', 'velocity': 0, 'midiClk': DrumConstants.SmallestGranularityInTicks, 'octaves': 3, 'pitch': "midi.C_3"  } 
                    cnt += 1

                
                currBeatNum += 1


        if ( 0 ) :
            print( "Fill Beats") 
            for beat in fillMeasure : 
                print ( beat, fillMeasure[beat] )  

        #fillMeasure => fillMeasure[item]

        return ( fillMeasure ) 

            
