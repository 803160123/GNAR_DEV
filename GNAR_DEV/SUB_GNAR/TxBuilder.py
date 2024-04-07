######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240312
# Purpose: Network TX TABLE BUILDER
# Functions: GNAR ATOLL Power
# Update: v1
# THIS IS A TEST MODULE FOR THE GNAR APPLICATION
######################################################################################

import pandas as pd
import datetime

TODAY = datetime.datetime.now()
TIMESTAMP = TODAY.strftime('%Y%m%d')

# FOR NOW DONT PASS A VARIABLE TO THE FUNCTION YET THIS IS A TEST
def builder() -> None:
    atolldict = {}
    siteName = 'UNL05835'
    nrSiteName = 'UNEN005835'
    lteSite = []
    nrSite = []
    lteTx = []
    nrTx =[]
    lteAntenna = []
    lteBand =  ['_7','_9','_2','_3']
    nrBand = ['_N005','_N077','_N077']
    faces = ['A','B','C','D']
    lsiz = (len(faces) * len(lteBand))
    nsiz = (len(faces) * len(nrBand))
    suffix = '_1_POD' 
    suffix2 = ['_1_POD','_2_POD']
    antennaAws = 'NNH4-65C-R6N17_2130MHz_02DT'
    antennaPcs = 'NNH4-65C-R6N17_1930MHz_02DT'
    antennaB12 = 'NNH4-65C-R6N17_725MHz_02DT'
    antennaWcs = 'NNH4-65C-R6N17_2355MHz_02DT'
    antennaCband = 'AIR6449_B77D_NR_BrM1_3820MHz_00DT'
    antennaDod = 'AIR6419-N77-BrM1_3500MHz_00DT'
    
    
    # GONNA GLUE THE NICKELS TOGETHER TO BUILD THE DICT{} BEFORE CONVERTING INTO A df
    # DO THE ANTENNAS AND THE ADDITIONAL COLUMNS IN THE df
    # COMBINE into one SITE AND ONE TX LIST PRIOR TO df

        
    # TEST TO BUILD DICT{}
    for _ in range(lsiz):
        lteSite.append(siteName)
    
    # print(lteSite)
    
    for i in range(len(lteBand)):
        for j in range(len(faces)):
           lteTx.append(f"{siteName}{lteBand[i]}{faces[j]}{suffix}")
          
    # print(lteTx)
    
    for _ in range(nsiz):
        nrSite.append(nrSiteName)
        
    for t in range(len(nrBand)):
        for s in range(len(faces)):
            nrTx.append(f"{nrSiteName}{nrBand[t]}{faces[s]}{suffix}")


    '''
    for _ in range(lsiz):
        testAntenna.append(f"{antenna1}")
              
    # print(testAntenna)
    '''
    
    atollDict = {'Site': lteSite, 'Transmitter': lteTx}
    

    atollDF = pd.DataFrame(atollDict)
    print(atollDF)
    '''
    message6 = ['ANTENNA SIMULATION DB -- REMEDIATION']
    msg6Dict = {'OPTION 6': message6}    
    msg6Df = pd.DataFrame(msg6Dict)
    print(msg6Df.to_markdown(tablefmt="grid", index=False))
    '''

    
    ''' EXAMPLE
    d = []
    for p in game.players.passing():
        d.append(
            {
                'Player': p,
                'Team': p.team,
                'Passer Rating':  p.passer_rating()
            }
    )

    pd.DataFrame(d)
    '''



    # END OF FUNCTION
        

    
    
