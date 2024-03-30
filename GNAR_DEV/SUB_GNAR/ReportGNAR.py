######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240324
# Purpose: Reusable GNAR reporting functions
# Functions: GNAR Reporting module, This is also where all of my logging mechanism is stored.
# Update: v1
# NOTE: 
# NEED TO ADD ALL EXCEPTION HANDLING
######################################################################################


import os
#import sys
import datetime
import logging 

def buildGnarDir():
    """ THIS FUNCTION WILL RUN IN MAIN AND WILL CHECK AND BUILD THE DAILY REPO FOR GNAR REPORTING """
    today = datetime.datetime.now()
    timeStamp = today.strftime('%Y%m%d')
    # timeStamp = today.strftime('%Y%m%d-%H%M%S')
    dailyDir = 'GNAR_REPORT_'+timeStamp
    repoDir = 'C:\\Users\\cp965x\\source\\repos\\GNAR_DEV\\GNAR_DEV\\SUB_GNAR\\'+dailyDir 
    

    if os.path.isdir(repoDir):
        # print("Daily GNAR REPORT directory exists")
        return repoDir
    else: 
        try:
            os.mkdir(repoDir)
            print(f"Directory '{repoDir}' created.")
            return repoDir
        except FileExistsError as ferr:
            print(f"Directory '{repoDir}' already exists.")
            logg.warning(f"Directory Warning {ferr} '{repoDir}' already exists.")
            
    # END OF GNAR DIR FUNCTION
    
def buildGnarFile(file: str) -> str:
    today = datetime.datetime.now()
    timeStamp2 = today.strftime('%Y%m%d-%H%M%S')
    masterDir = buildGnarDir()
    masterFile = f"{masterDir}\\GNAR_{file}_{timeStamp2}.csv"
    print(masterFile) 
    return masterFile

    # END OF GNAR FILE FUNCTION

### THE BELOW BLOCK OF CODE ALLOWS ME TO LOG ALL MY MODULES AND MAIN FROM IN THE SAME FILE BY CALLING THE HEADER INTO THE OTHER MODULES ###
# REFERENCE: https: //stackoverflow.com/questions/15727420/using-logging-in-multiple-modules

logg = logging
today = datetime.datetime.now()
timeStamp3 = today.strftime('%Y%m%d')
masterDir = buildGnarDir()
logFile = f"{masterDir}\\GNAR_LOG_{timeStamp3}.txt"
logg.basicConfig(filename=logFile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s)')

""" LOGGING REFERENCE
log.debug()
log.info()
log.warning()
log.error()
log.critical()
"""                     