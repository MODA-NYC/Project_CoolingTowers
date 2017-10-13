
import numpy as np
import pandas as pd
import sys



def GetBBLFromBIN(df,BIN_column,geoclient_instance , condoBBL = False, ):
    '''
    A wrapper function for the NYC geoclient that returns the BBL associated with a BIN for a given dataset of buildings.
    
    
    arguments:
    df -- the input dataframe object
    BIN_column -- the name of the column containing BINs (string)
    geoclient_instance -- a nyc_geoclient object with credentials
    condoBBL -- if True will attempt to return the condominum billing BBL for a building, if it exists
    
    returns:
    df -- the geocoded dataframe object
    GeoClient_Errors -- a list of any errors encountered by nyc_geoclient, for reference
    
    '''
    
    df['BBL'] = np.nan
    Error_GeoClient = list()
    
    for idx, row in df.iterrows():
        BIN = row[BIN_column]        
        api_data = geoclient_instance.bin(BIN)
        
        

        try:
            print api_data['buildingIdentificationNumber']
            if condoBBL:
		df['BBL'].ix[idx] = api_data['condominiumBillingBbl']
	    else:
		df['BBL'].ix[idx] = api_data['bbl']
            
        except:
            e = sys.exc_info()[0]
            print e;
            
            try: 
                print api_data['message'];
                log = [row[BIN_column], api_data['message']]
            except:
                log = [row[BIN_column],'no error message']
        
            Error_GeoClient.append(log)       
            del e;
        
    if len(Error_GeoClient) > 0:  
        GeoClient_Errors = pd.DataFrame(Error_GeoClient, columns = ['BBL','Error'])
        
    else:
        GeoClient_Errors = None
    
    return(df, GeoClient_Errors)
