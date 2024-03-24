######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240324
# Purpose: Reusable GNAR reporting functions
# Functions: GNAR Reporting module
# Update: v1
# NOTE: 
# NEED TO ADD ALL EXCEPTION HANDLING
######################################################################################


import os
#import sys
import datetime

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
        except FileExistsError:
            print(f"Directory '{repoDir}' already exists.")
            
    # END OF GNAR DIR FUNCTION
    
def buildGnarFile(file: str) -> str:
    today = datetime.datetime.now()
    timeStamp2 = today.strftime('%Y%m%d-%H%M%S')
    masterDir = buildGnarDir()
    masterFile = f"{masterDir}\\GNAR_{file}_{timeStamp2}.csv"
    print(masterFile) 
    return masterFile

    # END OF GNAR FILE FUNCTION