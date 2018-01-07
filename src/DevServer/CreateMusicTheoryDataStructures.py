from __future__ import print_function
import sys
import MusicTheory


#    'DsMajor' :  { 'obvious' : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP':  [ 'GMinor', 'CMinor' ] ,   #up four half steps or down three half steps , iii, or vi, third or the sixth chord
#                            'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP':  [ 'GsMajor', 'FMinor'], #up five half steps or up two half steps , IV or ii
#                            'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP':  [  'AsMajor' ], # one half step down, or seven hald steps up, vii D, V
#                            }, 
#              
#             'unusual' : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP':  [ 'FsMajor', 'BMajor', 'GMinor', 'CMinor' ] , #up three half steps and make it major, or  down four half steps 
#                            'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP':  [ 'GsMinor', 'GsMajor', 'FMinor'], # up five half steps but play the Minor, #up five half steps or up two half steps , IV or ii
#                           'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP':  [ 'CsMajor', 'AsMinor',  'AsMajor' ], # down two half steps and make a major, seven half steps up + Minor # one half step down, or seven half steps up, vii D, V
#                            },
#              
#              
#              'obscure' : { 'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP':  [ 'FsMajor', 'BMajor', 'GMinor', 'CMinor' ] , #up three half steps and make it major, or  down four half steps 
#                            'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP':  [ 'GsMinor', 'GsMajor', 'FMinor'], # up five half steps but play the Minor, #up five half steps or up two half steps , IV or ii
#                            'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP':  [ 'CsMajor', 'AsMinor',  'AsMajor' ], # down two half steps and make a major, seven half steps up + Minor # one half step down, or seven half steps up, vii D, V
#                            },
#              
#              },




Notes = [ "C", "Cs",  "D", "Ds",  "E",  "F", "Fs",  "G", "Gs",  "A", "As",  "B" ] ;

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
  'B' : 11 
  } ;
  

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
  11:'B'  , 
  } ;

def CreateChordProgressionJumps ( homeNote, chord ) : 


    homeIndex = NotesToPitch[homeNote] 


    minor = 'Minor'
    major = 'Major'
    dim   = 'Dim'
    Print = False

    #obvious jumps
    # small jumps
    indexA = ( homeIndex + 4 ) % 12       # up four half steps, minor
    indexB = ( homeIndex + ( 12-3) ) % 12 # down three half steps, minor
    chordASml = pitchToNotes[indexA] + minor
    chordBSml = pitchToNotes[indexB] + minor
    obviousSmlJumps = [ chordASml, chordBSml ] 
    StringSmlChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ '" + chordASml + "', '" + chordBSml + "' ], " 
        
    # mid jumps
    indexA = ( homeIndex + 5 ) % 12  # up five half steps, major
    indexB = ( homeIndex + 2 ) % 12  # up two half steps, minor
    chordAMid = pitchToNotes[indexA] + major
    chordBMid = pitchToNotes[indexB] + minor
    obviousMidJumps = [ chordAMid, chordBMid ] 
    StringMidChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': [ '" + chordAMid + "', '" + chordBMid + "' ], "     

    # big jumps
    indexA = ( homeIndex + (12-1) ) % 12  # down one half step, diminished
    indexB = ( homeIndex + 7 ) % 12  # up seven half steps, major
    chordABig = pitchToNotes[indexA] + dim
    chordBBig = pitchToNotes[indexB] + major
    obviousBigJumps = [ chordABig, chordBBig ] 
    StringBigChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': [ '" + chordABig + "', '" + chordBBig + "' ], "     
    StringObvious = "\t\t'obvious': {" + "\n" + StringSmlChordProgJump + "\n" + StringMidChordProgJump + "\n" + StringBigChordProgJump + "\n" + "\t\t\t}," + "\n"

    if ( Print ) : 
        print ( "Obvious Small Jump for chord", chord, ": ", obviousSmlJumps ) 
        print ( "Obvious Mid   Jump for chord", chord, ": ", obviousMidJumps ) 
        print ( "Obvious Big   Jump for chord", chord, ": ", obviousBigJumps ) 
        print ( StringObvious ) 


    #unusual jumps
    # small jumps
    indexA = ( homeIndex + 3 ) % 12       # up three half steps, major
    indexB = ( homeIndex + ( 12-4) ) % 12 # down four half steps, major
    chordCSml = pitchToNotes[indexA] + major
    chordDSml = pitchToNotes[indexB] + major
    unusualSmlJumps = [ chordCSml, chordDSml ] 
    StringSmlChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ '" + chordASml + "', '" + chordBSml + "', '" + chordCSml + "', '" + chordDSml + "' ], " 
        
    # mid jumps
    indexA = ( homeIndex + 5 ) % 12  # up five half steps, minor
    indexB = ( homeIndex + 2 ) % 12  # up two half steps, major
    chordCMid = pitchToNotes[indexA] + minor
    chordDMid = pitchToNotes[indexB] + major
    unusualMidJumps = [ chordCMid, chordDMid ] 
    StringMidChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': [ '" + chordAMid + "', '" + chordBMid + "', '" + chordCMid + "', '" + chordDMid + "' ], " 


    # big jumps
    indexA = ( homeIndex + (12-2) ) % 12  # down two half step, major
    indexB = ( homeIndex + 7 ) % 12  # up seven half steps, minor
    chordCBig = pitchToNotes[indexA] + major
    chordDBig = pitchToNotes[indexB] + minor
    unusualBigJumps = [ chordCBig, chordDBig ] 
    StringBigChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': [ '" + chordABig + "', '" + chordBBig + "', '" + chordCBig + "', '" + chordDBig + "' ], " 
    StringUnusual = "\t\t'unusual': {" + "\n" + StringSmlChordProgJump + "\n" + StringMidChordProgJump + "\n" + StringBigChordProgJump + "\n" + "\t\t\t}," + "\n"

    if ( Print ) : 
        print ( "Unusual Small Jump for chord", chord, ": ", unusualSmlJumps ) 
        print ( "Unusual Mid   Jump for chord", chord, ": ", unusualMidJumps ) 
        print ( "Unusual Big   Jump for chord", chord, ": ", unusualBigJumps ) 
        print ( StringUnusual ) 


    #obscure jumps
    # small jumps
    indexA = ( homeIndex + 3 ) % 12       # up three half steps, major
    indexB = ( homeIndex + ( 12-4) ) % 12 # down four half steps, major
    chordESml = pitchToNotes[indexA] + major
    chordFSml = pitchToNotes[indexB] + major
    obscureSmlJumps = [ chordESml, chordFSml ] 
    StringSmlChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_SML_JUMP': [ '" + chordESml + "', '" + chordFSml + "', '" + chordCSml + "', '" + chordDSml + "' ], "
        
    # mid jumps
    indexA = ( homeIndex + 5 ) % 12  # up five half steps, minor
    indexB = ( homeIndex + 2 ) % 12  # up two half steps, major
    chordEMid = pitchToNotes[indexA] + minor
    chordFMid = pitchToNotes[indexB] + major
    obscureMidJumps = [ chordEMid, chordFMid ] 
    StringMidChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_MID_JUMP': [ '" + chordEMid + "', '" + chordFMid + "', '" + chordCMid + "', '" + chordDMid + "' ], " 


    # big jumps
    indexA = ( homeIndex + (12-2) ) % 12  # down two half step, major
    indexB = ( homeIndex + 7 ) % 12  # up seven half steps, minor
    chordEBig = pitchToNotes[indexA] + major
    chordFBig = pitchToNotes[indexB] + minor
    obscureBigJumps = [ chordEBig, chordFBig ] 
    StringBigChordProgJump = "\t\t\t'PLAY_CHORD_PROGRESSION_TONE_BIG_JUMP': [ '" + chordEBig + "', '" + chordFBig + "', '" + chordCBig + "', '" + chordDBig + "' ], " 
    StringObscure = "\t\t'obscure': {" + "\n" + StringSmlChordProgJump + "\n" + StringMidChordProgJump + "\n" + StringBigChordProgJump + "\n" + "\t\t\t}," + "\n"

    if ( Print ) : 
        print ( "Obscure Small Jump for chord", chord, ": ", obscureSmlJumps ) 
        print ( "Obscure Mid   Jump for chord", chord, ": ", obscureMidJumps ) 
        print ( "Obscure Big   Jump for chord", chord, ": ", obscureBigJumps ) 
        print ( StringObscure ) 

    String = "\t'" + chord + "'" + " : { \n" + StringObvious + StringUnusual + StringObscure + '\t\t}, '
    print()
    print ( String ) 


def CreateScaleListForChords ( chord ) : 

    notesInChord      = MusicTheory.AllChords[chord]
    triadNotesInChord = [ notesInChord[0], notesInChord[1], notesInChord[2] ]

    scaleList = [] 
    scales = ' [ '

    if ( chord in MusicTheory.NotesInScale ) : 
        scaleList.append ( chord ) 
        scales += "'" + chord + "', " 
    elif ( chord.endswith('Maj7') ) : 
        homeNote = MusicTheory.AllChords[chord][0]
        scale = homeNote + 'Major'
        scaleList.append ( scale ) 
        scales += "'" + scale + "', " 
    elif ( chord.endswith('m7') ) : 
        homeNote = MusicTheory.AllChords[chord][0]
        scale = homeNote + 'Minor'
        scaleList.append ( scale ) 
        scales += "'" + scale + "', " 
    elif ( chord.endswith('7') ) : 
        homeNote = MusicTheory.AllChords[chord][0]
        scale = homeNote + 'Major'
        scaleList.append ( scale ) 
        scales += "'" + scale + "', " 
        

    for scale in MusicTheory.NotesInScale :
        
        if ( scale == chord ) : 
            continue

        if ( scale.endswith ( 'Oct' ) or scale.endswith ( 'Arabic' ) ) : 
             continue
        notesInScale = MusicTheory.NotesInScale[scale] 

        
        numCommonNotes      = len(list(set(notesInChord).intersection(notesInScale)))
        numCommonTriadNotes = len(list(set(triadNotesInChord).intersection(notesInScale)))
        numCommonNotes      = numCommonTriadNotes
        

        if ( numCommonNotes >= 3 ) :  # atleast the triad exists
            scaleList.append ( scale ) 
            scales += "'" + scale + "', " 


    scales += ' ], '
    scales = scales.replace( "',  ]", "' ]",  1 ) 
    String = "\t'" + chord + "': " + scales 

    #print ( scaleList ) 
    print ( String ) 


def CreatePentatonicScale ( scale ) : 
    if scale.endswith ( 'Major' ) : 
        noteList = [ 1, 2, 3, 5, 6 ]
    elif scale.endswith ( 'Minor' ) : 
        noteList = [ 1, 3, 4, 5, 7 ]
    else : 
        noteList = [ 1, 2, 3, 5, 6 ]

    String = "\t'" + scale + "': [" 
    for note in noteList : 
        strNote = "'" + MusicTheory.NotesInScale[scale][note-1] + "', "
        String += strNote

    String += " ], "
    String = String.replace( "',  ]", "' ]",  1 ) 

    print ( String ) 



def  CreateNeighborTonesForScale ( scale ) : 
    
    String = ""

    for note in MusicTheory.KeyDict[scale] : 
        index = MusicTheory.KeyDict[scale][note] 
        neighborToneIndex1 = ( index + 1 ) 
        if ( neighborToneIndex1 > 7 ) : 
            neighborToneIndex1 = 1 
        neighborToneIndex2 = ( index - 1 ) 
        if ( neighborToneIndex2 <= 0 ) : 
            neighborToneIndex2 = 7 
            
        neighborTone1 = MusicTheory.ReverseKeyDict[scale][neighborToneIndex1] 
        neighborTone2 = MusicTheory.ReverseKeyDict[scale][neighborToneIndex2] 
        String += "\t\t'" + note + "': [ " + "'" + neighborTone1 + "', '" +  neighborTone2 + "' ],\n" 
        
    String = "\t" + "'" + scale + "': {\n" + String + "\t}," 
    print ( String ) 

def  CreatePassingTonesForScale ( scale ) : 
    
    String = ""

    for note in MusicTheory.KeyDict[scale] : 
        index = MusicTheory.KeyDict[scale][note] 

        passingToneIndex1 = ( index + 1 ) 
        if ( passingToneIndex1 > 7 ) : 
            passingToneIndex1 = 1            
        passingToneIndex2 = ( passingToneIndex1 + 1 ) 
        if ( passingToneIndex2 > 7 ) : 
            passingToneIndex2 = 1

        passingTone1 =  MusicTheory.ReverseKeyDict[scale][passingToneIndex1] 
        passingTone2 =  MusicTheory.ReverseKeyDict[scale][passingToneIndex2] 


        passingToneIndex3 = ( index - 1 ) 
        if ( passingToneIndex3 <= 0 ) : 
            passingToneIndex3 = 7
        passingToneIndex4 = ( passingToneIndex3 - 1 ) 
        if ( passingToneIndex4 <= 0 ) : 
            passingToneIndex4 = 7
        passingToneIndex5 = ( passingToneIndex4 - 1 ) 
        if ( passingToneIndex5 <= 0 ) : 
            passingToneIndex5 = 7
            
        passingTone3 =  MusicTheory.ReverseKeyDict[scale][passingToneIndex3] 
        passingTone4 =  MusicTheory.ReverseKeyDict[scale][passingToneIndex4] 
        passingTone5 =  MusicTheory.ReverseKeyDict[scale][passingToneIndex5] 


        String += "\t\t'" + note + "': [ [ " + "'" + passingTone1 + "', '" +  passingTone2 + "' ], ['" + passingTone3 + "', '" +  passingTone4 + "', '" +  passingTone5 + "'] ],\n"   
        
    String = "\t" + "'" + scale + "': {\n" + String + "\t}," 
    print ( String ) 


def CreateOtherTonesForScale ( scale ) : 
    String = ""

    for note in MusicTheory.KeyDict[scale] : 
        index = MusicTheory.KeyDict[scale][note] 

        otherToneIndex = ( index + 3 ) 
        if ( otherToneIndex > 7 ) : 
            otherToneIndex = index - 4            

        otherTone = MusicTheory.ReverseKeyDict[scale][otherToneIndex] 


        String += "\t\t'" + note + "': [ '" + otherTone +  "'], \n"   
        
    String = "\t" + "'" + scale + "': {\n" + String + "\t}," 
    print ( String ) 
    

def ChordProgressionJumps () :

    for note in Notes : 
        chord = note + 'Major'        
        CreateChordProgressionJumps ( note, chord ) 

    print() 
    for note in Notes : 
        chord = note + 'Minor'        
        CreateChordProgressionJumps ( note, chord ) 

    print() 
    for note in Notes : 
        chord = note + 'Dim'        
        CreateChordProgressionJumps ( note, chord ) 


def ScaleListForChords () : 

    string = "ChordsToScale = { \n" 
    print ( string ) 
    for chord in MusicTheory.AllChords : 
        CreateScaleListForChords ( chord ) 
    string =  "\t}" 
    print (string)

def NeighborTonesForScale () : 

    for scale in MusicTheory.KeyDict : 
        CreateNeighborTonesForScale (  scale ) 
    print() 


def PassingTonesForScale () : 

    for scale in MusicTheory.KeyDict : 
        CreatePassingTonesForScale ( scale ) 
    print() 


def OtherTonesForScale () : 

    for scale in MusicTheory.KeyDict : 
        CreateOtherTonesForScale ( scale ) 
    print() 

def PentatonicScale () : 
    
    print ( "PentatonicScale = {" ) 

    for scale in MusicTheory.NotesInScale : 
        CreatePentatonicScale ( scale )

    print ( "\t}" ) 


def CreateChordToneToNextChordTone ( scale, chord ) :

    String = "\t\t" + "'" + scale + "': [ "
    chordNotes = MusicTheory.AllChords[chord]

    dataUp   = "[ "
    dataDown = "[ " 

    for i in range ( 3 ) : 

        note = chordNotes[i] 

        index = MusicTheory.KeyDict[scale][note] 

        CTtoNextCTIndex1 = index + 1 
        if ( CTtoNextCTIndex1 > 7 ) : 
            CTtoNextCTIndex1 = 1

        CTtoNextCTIndex2 = CTtoNextCTIndex1 + 1
        if ( CTtoNextCTIndex2 > 7 ) : 
            CTtoNextCTIndex2 = 1

        CTtoNextCTIndex3 = CTtoNextCTIndex2 + 1
        if ( CTtoNextCTIndex3 > 7 ) : 
            CTtoNextCTIndex3 = 1

        CTtoNextCT1 = MusicTheory.ReverseKeyDict[scale][CTtoNextCTIndex1]
        CTtoNextCT2 = MusicTheory.ReverseKeyDict[scale][CTtoNextCTIndex2]
        CTtoNextCT3 = MusicTheory.ReverseKeyDict[scale][CTtoNextCTIndex3]

        CTtoNextCTIndex4 = index - 1 
        if ( CTtoNextCTIndex4 <= 0 ) : 
            CTtoNextCTIndex4 = 7

        CTtoNextCTIndex5 = CTtoNextCTIndex4 - 1
        if ( CTtoNextCTIndex5 <= 0 ) : 
            CTtoNextCTIndex5 = 7

        CTtoNextCTIndex6 = CTtoNextCTIndex5 - 1
        if ( CTtoNextCTIndex6 <= 0 ) : 
            CTtoNextCTIndex6 = 7

        CTtoNextCT4 = MusicTheory.ReverseKeyDict[scale][CTtoNextCTIndex4]
        CTtoNextCT5 = MusicTheory.ReverseKeyDict[scale][CTtoNextCTIndex5]
        CTtoNextCT6 = MusicTheory.ReverseKeyDict[scale][CTtoNextCTIndex6]


        if ( i == 0 )  : 
            
            dataUp   += "['" + note + "', '" + CTtoNextCT1 + "', '" + CTtoNextCT2 + "'], "
            dataDown += "['" + note + "', '" + CTtoNextCT4 + "', '" + CTtoNextCT5 + "', '" + CTtoNextCT6 + "'], "

        elif ( i == 1 ) : 

            dataUp   += "['" + note + "', '" + CTtoNextCT1 + "', '" + CTtoNextCT2 + "'], "
            dataDown += "['" + note + "', '" + CTtoNextCT4 + "', '" + CTtoNextCT5 + "'], "

        elif ( i == 2 ) : 

            dataUp   += "['" + note + "', '" + CTtoNextCT1 + "', '" + CTtoNextCT2 + "', '" + CTtoNextCT3 + "'] "
            dataDown += "['" + note + "', '" + CTtoNextCT4 + "', '" + CTtoNextCT5 + "'] "


    dataUp   += " ]"
    dataDown += " ]"

    String += dataUp + ", " + dataDown + " ],"
    print ( String ) 


def ChordToneToNextChordTone () :

    print ( "ChordToneToNextChordTone = { " ) 
    for chord in MusicTheory.ChordsToScale : 
        print ( "\t'" + chord + "': {" ) 
        for scale in MusicTheory.ChordsToScale[chord] : 
            CreateChordToneToNextChordTone (  scale, chord ) 
        print ( "\t\t}, " ) 

    print ( "\t} " ) 
    


def Create7thAnd9thChords ( chord, homeIndex, adderIndex ) :
    
    String = "\t'" + chord + "' : [ '" + MusicTheory.pitchToNotes[homeIndex] + "', " 
    for index in adderIndex : 
        noteIndex = ( index + homeIndex ) % 12
        String += "'" + MusicTheory.pitchToNotes[noteIndex] + "', " 
    String += " ]," 
    String = String.replace( "',  ]", "' ]",  1 ) 
    print ( String ) 


def SeventhAndNinthChords () :
    
    print ( "ArpChords = { " )
    for chord in MusicTheory.AllChords : 
        
        homeNote  = MusicTheory.AllChords[chord][0]
        homeIndex = MusicTheory.NotesToPitch[homeNote]
        if ( chord.endswith ( 'Maj7' ) or chord.endswith ( 'Major' ) ) : 
            Create7thAnd9thChords ( chord, homeIndex, [4, 7, 9, 11, 14] ) 
        elif ( chord.endswith ( 'm7' ) or chord.endswith ( 'Minor' ) ) : 
            Create7thAnd9thChords ( chord, homeIndex, [3, 7, 8, 10, 14] ) 
        elif ( chord.endswith ( '7' ) ) : 
            Create7thAnd9thChords ( chord, homeIndex, [4, 7, 9, 10, 14] ) 
        elif ( chord.endswith ( 'Dim' ) ) : 
            Create7thAnd9thChords ( chord, homeIndex, [3, 6, 9, 0] ) 

    print ( "\t} " )


if __name__ == '__main__' : 


    #ChordProgressionJumps  () 
    #CreateChordProgressionJumps ( 'Ds', 'DsMajor' ) 
    #sys.exit(0) 


    ScaleListForChords () 
    #CreateScaleListForChords ( 'D', 'DDim' ) 
    sys.exit(0) 


    #NeighborTonesForScale () 
    #CreateNeighborTonesForScale (  'CMajor' ) 

    #PassingTonesForScale () 
    #CreatePassingTonesForScale (  'CMajor' ) 

    #OtherTonesForScale ()
    #CreateOtherTonesForScale (  'CMajor' ) 

    #PentatonicScale()
    #CreatePentatonicScale ( 'CMajor' ) 

    #ChordToneToNextChordTone ()
    #CreateChordToneToNextChordTone ( 'CMajor', 'Em7' ) 

    #SeventhAndNinthChords () 
    #Create7thAnd9thChords ( 'CMajor', 0, [4, 7, 11, 14] ) 
