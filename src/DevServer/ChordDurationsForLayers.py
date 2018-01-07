from __future__ import print_function
import sys
import Constants 


def createChordDurations ( duration ) :
    
    slowSplit = [] 
    mediumSplit = [] 
    fastSplit = [] 
    for minDur in Constants.MinChordDurationBreakdown : 
        mod = duration % minDur
        div = duration // minDur
        if ( mod == 0 ) : 
            split = [ minDur for i in range(div) ] 
        elif ( mod in Constants.MinChordDurationBreakdown )  : 
            split = [ minDur for i in range(div) ] 
            split.append ( mod ) 

        #print ( split ) 
        slow = False
        medium = False
        for dur in split : 
            if ( dur == 720 or dur == 960 ) : 
                slow = True
                medium = True
            if ( dur == 480 ) : 
                medium = True
                
        fastSplit.append ( split ) 
        if ( slow == True ) : 
            slowSplit.append ( split ) 
        if ( medium == True ) : 
            mediumSplit.append ( split ) 
        

    String = str(duration) + ": {"
    print ( String )

 
    print ( "\t'slow': ", slowSplit , ",") 
    print ( "\t'medium': ", mediumSplit, "," ) 
    print ( "\t'fast': ", fastSplit, "," ) 
    print ( "\t}," ) 
    
    #print ( "Duration: ", duration, "Splits: ", durationSplit ) 
    print() 

def ChordSplitDurations () :

    durations = [ 1200, 1440, 1920, 2160, 2880, 3840, 5760, 7680 ]
    durations = [ 2400, 3600, 4800 ] 
    durations = [ 3360, 5040, 4320 ] 
    durations = [ 6720 ] 
    for dur in durations : 
        createChordDurations ( dur ) 



if __name__ == '__main__' : 

    ChordSplitDurations () 
    #createChordDurations ( 1200 ) 
    #createChordDurations ( 1200 ) 
    #createChordDurations ( 3840 ) 
    #createChordDurations ( 5760 ) 
