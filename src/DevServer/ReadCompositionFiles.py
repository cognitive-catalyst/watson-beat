import collections

def ReadCompositionSettings ( self ) : 
        
    finName = "CompositionSettings" 
    fin = open ( finName, mode='r' ) 

    compositionSettings = collections.OrderedDict() 


    for line in fin : 
        line = line.rstrip() 

        #print ( "line: ", line ) 
        
        if ( line.startswith ( "Movement" ) ) : 

            data = line.split () 
            for item in range(0, len(data), 2)  : 
                if ( data[item] == 'Movement' ) : 
                    mvNum = int(data[item+1] ) 
                    compositionSettings[mvNum] = collections.OrderedDict() 


        elif ( line.startswith ( "SectionNum" ) ) : 

            data = line.split () 
            for item in range(0, len(data), 2)  : 
                #print ( item, data[item],  data[item+1] ) 
                if ( data[item] == 'SectionNum' ) : 
                    secNum = int(data[item+1] ) 
                    compositionSettings[mvNum][secNum] = collections.OrderedDict() 
                elif ( data[item] == 'NumPhrases' ) : 
                    numPhrases = int(data[item+1])
                    for ph in range(numPhrases) : 
                        compositionSettings[mvNum][secNum][ph] = {'clock': 0, 'mute': False }
                        #print ( "Section: ", secNum, "Phrase Num: ", ph ) 
                        
            
        elif ( line.startswith ( "StartofSection" ) ) : 

            data = line.split () 
            for item in range(0, len(data), 2)  : 
                #print ( "SoS: ", item, data[item],  data[item+1] ) 
                if ( data[item] == 'StartofSection' ) : 
                    secNum = int(data[item+1] ) 
                    #print ( "Sec Num: ", secNum ) 
                elif ( data[item] == 'PhraseNum' ) : 
                    phNum = int(data[item+1] ) 
                    #print ( "Phrase Num: ", phNum ) 
                elif ( data[item] == 'Clock' ) : 
                    compositionSettings[mvNum][secNum][phNum]['clock'] = int(data[item+1] )  
                elif ( data[item] == 'Mute' ) : 
                    compositionSettings[mvNum][secNum][phNum]['mute'] = data[item+1]
                    

    fin.close() 


    print() 
    print() 
    for mvNum in compositionSettings : 
        print ( "Movement: ", mvNum ) 
        for sec in compositionSettings[mvNum] : 
            print ( "Section: ", sec ) 
            for ph in compositionSettings[mvNum][sec] : 
                print ( "phrase: ", ph, "Clock: ", compositionSettings[mvNum][sec][ph]['clock'], "Mute: ", compositionSettings[mvNum][sec][ph]['mute'] ) 



    return ( compositionSettings ) 
