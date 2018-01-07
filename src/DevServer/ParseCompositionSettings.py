
from __future__ import print_function
import collections

Movement = collections.OrderedDict()

def parseCompositionSettings ( finName ) :

    fin = open ( finName, mode='r' ) 

    for line in fin : 
        line = line.rstrip() 

        #print ( "line: ", line ) 
        
        if ( line.startswith ( "Movement" ) ) : 
            data = line.split () 
            for item in range(0, len(data), 2)  : 
                if ( data[item] == 'Movement' ) : 
                    mvNum = int(data[item+1] ) 
                    Movement[mvNum] = collections.OrderedDict()
                    Movement[mvNum]['Sections'] = collections.OrderedDict()

                elif ( data[item] == 'NumSections' ) : 
                    Movement[mvNum]['numSections'] = int(data[item+1] ) 
                
                elif ( data[item] == 'Mood' ) : 
                    Movement[mvNum]['mood'] = data[item+1]

                elif ( data[item] == 'type' ) : 
                    Movement[mvNum]['type'] = data[item+1]

        elif ( line.startswith ( "SectionNum" ) ) : 

            data = line.split () 
            for item in range(0, len(data), 2)  : 
                #print ( item, data[item],  data[item+1] ) 
                if ( data[item] == 'SectionNum' ) : 
                    secNum = int(data[item+1] ) 
                    Movement[mvNum]['Sections'][secNum] = collections.OrderedDict()

                elif ( data[item] == 'NumPhrases' ) : 
                    numPhrases = int(data[item+1])
                    Movement[mvNum]['Sections'][secNum]['numPhrases'] = numPhrases 
                    Movement[mvNum]['Sections'][secNum]['Phrases'] = collections.OrderedDict()

                elif ( data[item] == 'NumChords' ) : 
                    numChords = int(data[item+1])
                    Movement[mvNum]['Sections'][secNum]['numChords'] = numChords

        elif ( line.startswith ( "SectionLayers" ) ) : 

            data = line.split () 
            lyr = []            
            layers = data[1].replace ( "[", "" ) 
            layers = layers.replace ( "]", "" ) 
            layers = layers.replace ( ",", " " ) 
            layers = layers.replace ( "'", "" ) 
            layers = layers.split ( )
            for l in layers : 
                lyr.append ( l ) 
            Movement[mvNum]['Sections'][secNum]['layers'] = lyr
            #print ( "SecId", secNum, "layers:", lyr, Movement[mvNum]['Sections'][secNum]['layers'] ) 
            #print() 

        elif ( line.startswith ( "Phrase" ) ) : 

            data = line.split () 
            for item in range(0, len(data), 2)  : 
                #print ( item, data[item],  data[item+1] ) 
                if ( data[item] == 'PhraseNum' ) : 
                    phNum = int(data[item+1] ) 
                    Movement[mvNum]['Sections'][secNum]['Phrases'][phNum] = collections.OrderedDict()

                elif ( data[item] == 'StartClk' ) : 
                    startClk = int(data[item+1] ) 
                    Movement[mvNum]['Sections'][secNum]['Phrases'][phNum]['startClk'] = startClk 

                elif ( data[item] == 'EndClk' ) : 
                    endClk = int(data[item+1] ) 
                    Movement[mvNum]['Sections'][secNum]['Phrases'][phNum]['endClk'] = endClk 

                elif ( data[item] == 'Layers' ) : 
                    layers = (data[item+1] ) 
                    layers = layers.replace ( "]" , "" ) 
                    layers = layers.replace ( "[" , "" ) 
                    layers = layers.replace ( "'", "" ) 
                    layers = layers.replace ( "," , " " ) 

                    
                    layers = layers.split ( )
                    lyr = []
                    for l in layers : 
                        lyr.append ( l ) 
                    Movement[mvNum]['Sections'][secNum]['Phrases'][phNum]['layers'] = lyr

            

def getLayersForSection ( mvNum, secNum ) : 
    #print ( "Layers for Movement: ", mvNum, "Section: ", secNum , Movement[mvNum]['Sections'][secNum]['layers'] ) 
    #print() 
    return Movement[mvNum]['Sections'][secNum]['layers'] 
    

def getLayersForPhrase ( mvNum, secNum, phNum ) : 
    #print ( "Layers for Movement: ", mvNum, "Section: ", secNum , "Phrase: ", phNum, Movement[mvNum]['Sections'][secNum]['Phrases'][phNum]['layers'] ) 
    #print()
    return Movement[mvNum]['Sections'][secNum]['Phrases'][phNum]['layers'] 

if __name__ == '__main__' : 

    finName = "../CompositionSettings" 
    parseCompositionSettings ( finName ) 

    # to get number of sections in movement 0
    numSections = Movement[0]['numSections']

    # to get number of phrases in section 0 in movement 0
    numPhrases = Movement[0]['Sections'][0]['numPhrases']

    # to get the layers for section 3 in movement 0
    layers = getLayersForSection ( 0, 3 ) 

    # to get the layers for phrase 1 in section 4 in movement 0
    layers = getLayersForSection ( 0, 4, 1 ) 



    layers = getLayersForSection ( 0, 0 )   # getLayersForSection ( movementNumber, sectionNumber )   # 
    layers = getLayersForSection ( 0, 1 ) 
    layers = getLayersForSection ( 0, 2 ) 
    layers = getLayersForSection ( 0, 3 ) 


    layers = getLayersForPhrase ( 0, 0, 0 ) 
    layers = getLayersForPhrase ( 0, 4, 0 ) 
    layers = getLayersForPhrase ( 0, 4, 1 ) 
                        
