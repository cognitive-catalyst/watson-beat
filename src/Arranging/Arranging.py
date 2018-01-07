from __future__ import print_function

import collections

class Arranging : 

    def __init__ ( self, mood, layers, useDefault ) : 

        self.mood   = mood
        self.layers = layers 

        self.InitializeDefaultLayers ( layers, useDefault )
        self.InitializeLayersBasedOnMoods ( layers ) 

    def InitializeLayersBasedOnMoods ( self, Layers ) : 

        self.Layers = collections.OrderedDict () 
        for layer in Layers : 
            self.Layers[layer] = self.DefaultLayers[layer] 
            
        self.LayersBasedOnRange   = { 'low': {}, 'mid': {}, 'midToHi': {}, 'hi':{}, 'all': {} }
        self.LayersBasedOnDensity = { 1: {}, 2: {}, 3: {} } 

        self.LayersBasedOnRangeAndDensity = { 'low': {}, 'mid': {}, 'midToHi': {}, 'hi':{}, 'all': {} }
        for range in self.LayersBasedOnRangeAndDensity : 
            for density in self.LayersBasedOnDensity : 
                self.LayersBasedOnRangeAndDensity[range][density] = {}


        self.LayersBasedOnDensityAndRange = { 1: {}, 2: {}, 3: {} }  
        for density in self.LayersBasedOnDensityAndRange : 
            for range in self.LayersBasedOnRange : 
                self.LayersBasedOnDensityAndRange[density][range] = {} 


        for lyr in  self.Layers : 
            range   = self.Layers[lyr]['range']             
            density = self.Layers[lyr]['density']             

            self.LayersBasedOnRange[range][lyr]     = self.Layers[lyr]
            self.LayersBasedOnDensity[density][lyr] = self.Layers[lyr]

            self.LayersBasedOnDensityAndRange[density][range][lyr] = self.Layers[lyr]
            self.LayersBasedOnRangeAndDensity[range][density][lyr] = self.Layers[lyr]



    def InitializeDefaultLayers ( self, layers, useDefault ) : 



        if ( useDefault ) : 
        
            layers = [ 'bass1', 'bass2', 'loStrings', 'drumsBass', 'drumsKick', 'leftPianoBass', 
                       'rightPiano', 'piano1', 'rhythmChords', 'mel5', 'midStrings', 'drumsSnare' ]

            self.DefaultLayers = collections.OrderedDict () 

            self.DefaultLayers['bass1'] = { 'range': 'low', 'density': 1, 'type': '' }
            self.DefaultLayers['bass2'] = { 'range': 'low', 'density': 1, 'type': '' }
            self.DefaultLayers['loStrings'] = { 'range': 'low', 'density': 1, 'type': '' }

            self.DefaultLayers['drumsBass'] = { 'range': 'low', 'density': 1, 'type': 'percussion' }
            self.DefaultLayers['drumsKick'] = { 'range': 'low', 'density': 1, 'type': 'percussion' }
                   
            self.DefaultLayers['leftPianoBass'] = { 'range': 'low', 'density': 1, 'type': '' }


            self.DefaultLayers['piano1'] = { 'range': 'all', 'density': 3, 'type': '' }
            self.DefaultLayers['fillsForDrums'] = { 'range': 'all', 'density': 2, 'type': 'percussion' }


            self.DefaultLayers['rightPiano'] = { 'range': 'mid', 'density': 1, 'type': '' }
            self.DefaultLayers['midStrings'] = { 'range': 'mid', 'density': 2, 'type': '' }
            self.DefaultLayers['drumsSnare'] = { 'range': 'mid', 'density': 2, 'type': 'percussion' }
            self.DefaultLayers['drumsKit'] = { 'range': 'mid', 'density': 2, 'type': 'percussion' }


            self.DefaultLayers['rhythmChords'] = { 'range': 'midToHi', 'density': 2, 'type': '' }
            self.DefaultLayers['mel5'] = { 'range': 'midToHi', 'density': 2, 'type': 'melody' }
            self.DefaultLayers['arpStrings'] = { 'range': 'midToHi', 'density': 2, 'type': '' }


            self.DefaultLayers['drumsHihat'] = { 'range': 'hi', 'density': 1, 'type': 'percussion' }
            self.DefaultLayers['hiStrings'] = { 'range': 'hi', 'density': 1, 'type': '' }
            self.DefaultLayers['drumsCymbalSwell'] = { 'range': 'hi', 'density': 2, 'type': 'percussion' }
        
        else :
            
            self.DefaultLayers = layers 

        self.DefaultLayersBasedOnRange   = { 'low': {}, 'mid': {}, 'midToHi': {}, 'hi':{}, 'all': {} }
        self.DefaultLayersBasedOnDensity = { 1: {}, 2: {}, 3: {} } 



        self.DefaultLayersBasedOnRangeAndDensity = { 'low': {}, 'mid': {}, 'midToHi': {}, 'hi':{}, 'all': {} }
        for range in self.DefaultLayersBasedOnRangeAndDensity : 
            for density in self.DefaultLayersBasedOnDensity : 
                self.DefaultLayersBasedOnRangeAndDensity[range][density] = {}




        self.DefaultLayersBasedOnDensityAndRange = { 1: {}, 2: {}, 3: {} }  
        for density in self.DefaultLayersBasedOnDensityAndRange : 
            for range in self.DefaultLayersBasedOnRange : 
                self.DefaultLayersBasedOnDensityAndRange[density][range] = {} 



        for lyr in  self.DefaultLayers : 
            range   = self.DefaultLayers[lyr]['range']             
            density = self.DefaultLayers[lyr]['density']             

            self.DefaultLayersBasedOnRange[range][lyr]     = self.DefaultLayers[lyr]
            self.DefaultLayersBasedOnDensity[density][lyr] = self.DefaultLayers[lyr]

            self.DefaultLayersBasedOnDensityAndRange[density][range][lyr] = self.DefaultLayers[lyr]
            self.DefaultLayersBasedOnRangeAndDensity[range][density][lyr] = self.DefaultLayers[lyr]



        if ( 0 ) : 
            print ( "Layers Based on Density" ) 
            for density in self.DefaultLayersBasedOnDensity : 
                print ( "\tDensity: ", density ) 
                for lyr in self.DefaultLayersBasedOnDensity[density] : 
                    print  ( "\t\tLayer: ", lyr ) 
                print() 

        if ( 0 ) : 
            print ( "Layers Based on Range" ) 
            for range in self.DefaultLayersBasedOnRange : 
                print ( "\tRange: ", range ) 
                for lyr in self.DefaultLayersBasedOnRange[range] : 
                    print  ( "\t\tLayer: ", lyr ) 
                print() 

        if ( 0 ) : 
            print ( "Layers Based on Density And Range" ) 
            for density in self.DefaultLayersBasedOnDensityAndRange : 
                print ( "\tDensity: ", density ) 
                for range in self.DefaultLayersBasedOnDensityAndRange[density] :  
                    print ( "\t\tRange: ", range ) 
                    for lyr in self.DefaultLayersBasedOnDensityAndRange[density][range] :  
                        print  ( "\t\t\tLayer: ", lyr ) 
                    print() 


        if ( 0 ) : 
            print ( "Layers Based on Range And Density" ) 
            for range in self.DefaultLayersBasedOnRangeAndDensity : 
                print ( "\tRange: ", range ) 
                for density in self.DefaultLayersBasedOnRangeAndDensity[range] :  
                    print ( "\t\tDensity: ", density ) 
                    for lyr in self.DefaultLayersBasedOnRangeAndDensity[range][density] :  
                        print  ( "\t\t\tLayer: ", lyr ) 
                    print() 
