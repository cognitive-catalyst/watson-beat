from __future__ import print_function

import os
import sys
import json
import Section
import collections

def run ( wbClientJsonData, midiFile ) : 
    
    movementsServer = collections.OrderedDict() 
    
    wbClientMovements = collections.OrderedDict ( json.loads (wbClientJsonData) ) 

    for mvNum in wbClientMovements : 
        numUniqCPs = len(wbClientMovements[(mvNum)])
        movementsServer[mvNum] = collections.OrderedDict()  

        for uniqCPId in wbClientMovements[mvNum] : 

            section = Section.Section ( wbClientMovements[mvNum][uniqCPId]['wbLevers'], midiFile ) 
            movementsServer[mvNum][uniqCPId] = collections.OrderedDict(section.run () )

        if ( 1 ) :             
            for uniqCPId in wbClientMovements[mvNum] : 
                print ( "Dev Server Movement : ", mvNum, "Uniq Id: ", uniqCPId ) 
                for layer in movementsServer[mvNum][uniqCPId] : 
                    print ( "\tlayer: ", layer ) 
                    for chId in movementsServer[mvNum][uniqCPId][layer][0]  : 
                        print ( "\t\tChord Id: ", chId ) 
                        for item in movementsServer[mvNum][uniqCPId][layer][0][chId] :
                            print ( "\t\t\t" ,  item )
            
                    print() 
                print() 

    #print ( movementsServer.items()) 
    return json.dumps(movementsServer)

    sys.exit(0) 



    for mvNum in movements : 
        sectionsObj = movements[mvNum]['SectionsObj'].mood        
        numUniqCPs  = sectionsObj.numUniqCPs  
    
        movementsServer[mvNum] = collections.OrderedDict()  


        for uniqCPId in range(numUniqCPs) : 
            pl     = sectionsObj.uniqCPSettings[uniqCPId]['pl'] 
            key    = sectionsObj.uniqCPSettings[uniqCPId]['scale'] 
            tse    = sectionsObj.uniqCPSettings[uniqCPId]['tse'] 
            cpSeq  = sectionsObj.uniqCPSettings[uniqCPId]['cpSeq'] 
            layers = sectionsObj.layers 

            mood  = movements[mvNum]['mood'] 
            complexity = movements[mvNum]['complexity'] 
                
            wbLevers = {
                'id'          : uniqCPId,
                
                'phraseLength': pl,
                'tse'         : tse, 
                'primaryScale': key,
                'bassRhy'     : cpSeq,
                
                'mood'        : mood,
                'complexity'  : complexity, 
                
                'layers'      : layers, 

                    
                }
            
            section = Section.Section ( wbLevers, midiFile ) 
            movementsServer[mvNum][uniqCPId] = collections.OrderedDict(section.run () )

        if ( 1 ) :             
            for uniqCPId in range(numUniqCPs) : 
                print ( "Dev Server Movement : ", mvNum, "Uniq Id: ", uniqCPId ) 
                for layer in movementsServer[mvNum][uniqCPId] : 
                    print ( "\tlayer: ", layer ) 
                    for chId in movementsServer[mvNum][uniqCPId][layer][0]  : 
                        print ( "\t\tChord Id: ", chId ) 
                        for item in movementsServer[mvNum][uniqCPId][layer][0][chId] :
                            print ( "\t\t\t" ,  item )
            
                    print() 
                print() 


    #print ( movementsServer.items()) 
    return json.dumps(movementsServer)

