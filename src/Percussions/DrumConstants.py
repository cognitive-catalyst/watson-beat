
import random
import collections
from Skeleton import MusicTheory

DrumStyle = { 'groove' :{}, 'build': {}, 'fill':{} }

# all durations in ticks, assuming a resolution of 480


BeatInfo = {

    '3/4' : { 
        1:  { 'kick' : { 'probMax': 90, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 60 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'bass' : { 'probMax': 95, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 60 }, 
              },

        2:  { 'kick' : { 'probMax': 1,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
             },

        3:  { 'kick' : { 'probMax': 20, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 60, 'probMin': 50, 'velocityMax': 70, 'velocityMin':  30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        4:  { 'kick' : { 'probMax': 3,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
             },

        5:  { 'kick' : { 'probMax': 60, 'probMin': 50, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'hihat': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'bass' : { 'probMax': 25, 'probMin': 10, 'velocityMax': 120, 'velocityMin': 70 }, 
              },

        6:  { 'kick' : { 'probMax': 1,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
             },

        7:  { 'kick' : { 'probMax': 20, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 60, 'probMin': 50, 'velocityMax': 70, 'velocityMin':  30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        8:  { 'kick' : { 'probMax': 3,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        9:  { 'kick' : { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'bass' : { 'probMax': 50, 'probMin': 30, 'velocityMax': 120, 'velocityMin': 70 }, 
              },

        10: { 'kick' : { 'probMax': 1,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        11:  { 'kick' : { 'probMax': 20, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 60, 'probMin': 50, 'velocityMax': 70, 'velocityMin':  30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        12: { 'kick' : { 'probMax': 3,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        }, # end '3/4'


    
    '4/4' : { 
        1:  { 'kick' : { 'probMax': 90, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 60 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'bass' : { 'probMax': 95, 'probMin': 80, 'velocityMax': 120, 'velocityMin': 60 }, 
              },

        2:  { 'kick' : { 'probMax': 1,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
             },

        3:  { 'kick' : { 'probMax': 20, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 60, 'probMin': 50, 'velocityMax': 70, 'velocityMin':  30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        4:  { 'kick' : { 'probMax': 3,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
             },

        5:  { 'kick' : { 'probMax': 60, 'probMin': 50, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'hihat': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'bass' : { 'probMax': 25, 'probMin': 10, 'velocityMax': 120, 'velocityMin': 70 }, 
              },

        6:  { 'kick' : { 'probMax': 1,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
             },

        7:  { 'kick' : { 'probMax': 20, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 60, 'probMin': 50, 'velocityMax': 70, 'velocityMin':  30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        8:  { 'kick' : { 'probMax': 3,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        9:  { 'kick' : { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'bass' : { 'probMax': 50, 'probMin': 30, 'velocityMax': 120, 'velocityMin': 70 }, 
              },

        10: { 'kick' : { 'probMax': 1,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        11:  { 'kick' : { 'probMax': 20, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
               'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
               'hihat': { 'probMax': 60, 'probMin': 50, 'velocityMax': 70, 'velocityMin':  30 }, 
               'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        12: { 'kick' : { 'probMax': 3,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        13: { 'kick' : { 'probMax': 60, 'probMin': 50, 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'hihat': { 'probMax': 80, 'probMin': 70, 'velocityMax': 120, 'velocityMin': 60 }, 
              'bass' : { 'probMax': 25, 'probMin': 10, 'velocityMax': 120, 'velocityMin': 70 }, 
              },

        14: { 'kick' : { 'probMax': 1,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        15:  { 'kick' : { 'probMax': 20, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
               'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
               'hihat': { 'probMax': 60, 'probMin': 50, 'velocityMax': 70, 'velocityMin':  30 }, 
               'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
              },

        16: { 'kick' : { 'probMax': 3,  'probMin': 1 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'snare': { 'probMax': 30, 'probMin': 10, 'velocityMax': 70,  'velocityMin': 30 }, 
              'hihat': { 'probMax': 5 , 'probMin': 3 , 'velocityMax': 70,  'velocityMin': 30 }, 
              'bass' : { 'probMax': 1,  'probMin': 1,  'velocityMax': 70,  'velocityMin': 30 }, 
             },
        } # end '4/4'

    } # end TSEs




# TO DO: Works only for 4/4. Make it customizable
DrumBeat = { "Eighth"        : { 'numBeats': 8,  'ticks': 240 },      
             "Sixteenth"     : { 'numBeats': 16, 'ticks': 120 },      
             "Quarter"       : { 'numBeats': 4,  'ticks': 480 },      
             "half"          : { 'numBeats': 2,  'ticks': 960 },      
             "full"          : { 'numBeats': 1,  'ticks': 1920 },      
             "threeQuarters" : { 'numBeats': 12, 'ticks': 1440 }, 
     }






SmallestGranularityInTicks = 120 # TO DO: Works only for 4/4. Make it customizable
hihatMiniMeasure = random.randint ( 4, 8 ) # TO DO: Works only for 4/4. Make it customizable
maxBeatsInMeasure = 16  # TO DO: Works only for 4/4. Make it customizable
AccentedBeats = { 1: True, 2: False, 3: True, 4: False, 5: True, 6: False, 7: True, 8: False, 9: True, 10: False, 11: True, 12: False, 13: True, 14: False, 15: True, 16: False }
AllBeats = { 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True }

StrongAccentedBeats = { 1: True, 2: False, 3: False, 4: False, 5: True, 6: False, 7: False, 8: False, 9: True, 10: False, 11: False, 12: False, 13: True, 14: False, 15: False, 16: False }
WeakAccentedBeats = { 1: False, 2: False, 3: True, 4: False, 5: False, 6: False, 7: True, 8: False, 9: False, 10: False, 11: True, 12: False, 13: False, 14: False, 15: True, 16: False }




hihatPieces      =  [ 'hihat-closed', 'hihat-open', 'hihat-foot' ]
#hihatPiecesProbs = [ 'hihat-closed', 'hihat-open', 'hihat-closed', 'hihat-foot', 'hihat-closed', 'hihat-open', 'hihat-closed','hihat-foot', 'hihat-closed', 'hihat-foot' ]
hihatPiecesProbs      =  [ 'hihat-closed', 'hihat-open', 'hihat-foot' ]


fillPieces = { 'high' : [ 'crash', 'ride', 'hihat-closed', 'hihat-open', 'hihat-foot' ], 
               'mid'  : [ 'hitom', 'midtom', 'snare' ],
               'low'  : [ 'floortom', 'kick', 'bass' ]
               }

fillNotes = { 'high': { 'crash': 'Cs', 'ride': 'E', 'hihat-closed': 'Fs', 'hihat-open': 'As', 'hihat-foot': 'Gs', 'cymbal': 'A' },
              'mid':  { 'hitom': 'C', 'midtom': 'B', 'snare': 'D' },
              'low':  { 'floortom': 'F', 'kick': 'C', 'bass': 'C' }
               }


fillNoteOctaves = { 'high': { 'crash': '4', 'ride': '4', 'hihat-closed': '3', 'hihat-open': '3', 'hihat-foot': '3', 'cymbal': '6' },
                    'mid':  { 'hitom': '4', 'midtom': '3', 'snare': '3' },
                    'low':  { 'floortom': '3', 'kick': '3', 'bass': '3' }
               }


def getBeatsForKickDrum ( percussion )  :
    
    # Divide measure into 16 beats. assigning each beat a probability. 
    # TO DO: Works only for 4/4. Make it customizable
    beatCanPlay = { 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True }
    if ( percussion == 'super_slow' ) : 
        beatCanPlay = StrongAccentedBeats
    elif ( percussion == 'slow' ) : 
        beatCanPlay = AccentedBeats        
    else : 
        beatCanPlay = AllBeats

        
    beatData =  { 1: { 'probability': 90, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[1]  }, 
                  2: { 'probability': 1, 'intensity': 'weak', 'velocity': random.randint(30, 70),     'playBeat': beatCanPlay[2]  },
                  3: { 'probability': 20, 'intensity': 'weak', 'velocity': random.randint(30, 70),    'playBeat': beatCanPlay[3]  }, 
                  4: { 'probability': 3, 'intensity': 'weak', 'velocity': random.randint(30, 70),     'playBeat': beatCanPlay[4]  }, 
                  5: { 'probability': 60, 'intensity': 'weak', 'velocity': random.randint(30, 70),    'playBeat': beatCanPlay[5]  },
                  6: { 'probability': 1, 'intensity': 'weak', 'velocity': random.randint(30, 70),     'playBeat': beatCanPlay[6]  },
                  7: { 'probability': 20, 'intensity': 'weak', 'velocity': random.randint(30, 70),    'playBeat': beatCanPlay[7]  },
                  8: { 'probability': 3, 'intensity': 'weak', 'velocity': random.randint(30, 70),     'playBeat': beatCanPlay[8]  }, 
                  9: { 'probability': 80, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[9]  },
                  10: { 'probability': 1, 'intensity': 'weak', 'velocity': random.randint(30, 70),    'playBeat': beatCanPlay[10] },
                  11: { 'probability': 20, 'intensity': 'weak', 'velocity': random.randint(30, 70),   'playBeat': beatCanPlay[11] },
                  12: { 'probability': 3, 'intensity': 'weak', 'velocity': random.randint(30, 70),    'playBeat': beatCanPlay[12] }, 
                  13: { 'probability': 60, 'intensity': 'weak', 'velocity': random.randint(30, 70),   'playBeat': beatCanPlay[13] },
                  14: { 'probability': 1, 'intensity': 'weak', 'velocity': random.randint(30, 70),    'playBeat': beatCanPlay[14] },
                  15: { 'probability': 20, 'intensity': 'weak', 'velocity': random.randint(30, 70),   'playBeat': beatCanPlay[15] },
                  16: { 'probability': 3, 'intensity': 'weak', 'velocity': random.randint(30, 70),    'playBeat': beatCanPlay[16] }, 
                  
                  }



    return beatData



def getBeatsForSnareDrum ( percussion )  :
    

    # Divide measure into 16 beats. assigning each beat a probability. 
    # TO DO: Works only for 4/4. Make it customizable

    beatCanPlay = { 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True }
    if ( percussion == 'super_slow' ) : 
        beatCanPlay = StrongAccentedBeats
    elif ( percussion == 'slow' ) : 
        beatCanPlay = AccentedBeats        
    else : 
        beatCanPlay = AllBeats


    minProbUpBeats = 10 
    maxProbUpBeats = 30 

    
    beatData =  collections.OrderedDict () 
    beatData[5]  =  { 'probability': 80, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[5] }
    beatData[13] =  { 'probability': 80, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[13] }
    beatData[1]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[1]  }
    beatData[2]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[2]  }
    beatData[3]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[3]  }
    beatData[4]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[4]  }
    beatData[6]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[6]  }
    beatData[7]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[7]  }
    beatData[8]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[8]  }
    beatData[9]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70),  'playBeat': beatCanPlay[9]  }
    beatData[10]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70), 'playBeat': beatCanPlay[10] }
    beatData[11]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70), 'playBeat': beatCanPlay[11]}
    beatData[12]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70), 'playBeat': beatCanPlay[12]}
    beatData[14]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70), 'playBeat': beatCanPlay[14] }
    beatData[15]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70), 'playBeat': beatCanPlay[15] }
    beatData[16]  =  { 'probability': random.randint ( minProbUpBeats, maxProbUpBeats ), 'intensity': 'weak', 'velocity': random.randint(30, 70), 'playBeat': beatCanPlay[16] }


    return beatData


def getBeatsForHihatDrum (  percussion  )  :
    
    # Divide measure into 16 beats. assigning each beat a probability. 
    # TO DO: Works only for 4/4. Make it customizable

    beatCanPlay = { 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True }
    if ( percussion == 'super_slow' ) : 
        beatCanPlay = StrongAccentedBeats
    elif ( percussion == 'slow' ) : 
        beatCanPlay = AccentedBeats        
    else : 
        beatCanPlay = AllBeats


    beatData =  collections.OrderedDict ( { 1:  { 'probability': 80, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[1]  }, 
                                            2:  { 'probability': 5, 'intensity': 'weak', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[2]  }, 
                                            3:  { 'probability': 60, 'intensity': 'weak', 'velocity': random.randint(30, 70)   , 'playBeat': beatCanPlay[3]  }, 
                                            4:  { 'probability': 5, 'intensity': 'waek', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[4]  },
                                                                                                                                
                                            5:  { 'probability': 80, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[5]  },                                               
                                            6:  { 'probability': 5, 'intensity': 'weak', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[6]  },
                                            7:  { 'probability': 60, 'intensity': 'weak', 'velocity': random.randint(30, 70)   , 'playBeat': beatCanPlay[7]  }, 
                                            8:  { 'probability': 5, 'intensity': 'weak', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[8]  },
                                                                                                                                
                                            9:  { 'probability': 80, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[9]  },
                                            10: { 'probability': 5, 'intensity': 'weak', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[10] }, 
                                            11: { 'probability': 60, 'intensity': 'weak', 'velocity': random.randint(30, 70)   , 'playBeat': beatCanPlay[11] },
                                            12: { 'probability': 5, 'intensity': 'weak', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[12] }, 
                                                                                                                                
                                            13: { 'probability': 80, 'intensity': 'strong', 'velocity': random.randint(60, 120), 'playBeat': beatCanPlay[13] },
                                            14: { 'probability': 5, 'intensity': 'weak', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[14] },
                                            15: { 'probability': 60, 'intensity': 'weak', 'velocity': random.randint(30, 70)   , 'playBeat': beatCanPlay[15] },
                                            16: { 'probability': 5, 'intensity': 'weak', 'velocity': random.randint(30, 70)    , 'playBeat': beatCanPlay[16] }, 
                                                                                                                                
                                            }                                                                                   
                                          )                                                                                    
                                                                                                                               
                                                                                                                               
                                                                                                                               
    return beatData                                                                                                            
                                                                                                                               
                                                                                                                               
                                                                                                                               
                                                                                                                               
                                                                                                                               
                                                                                                                               
