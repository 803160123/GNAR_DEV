######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240210
# Purpose: GNAR - General Netowork Audit and Remediation main function 
# Functions: main()
# Update: v0.1
# Notes:
######################################################################################

#import os
#import sys
#import datetime
#import pandas as pd
#import numpy as np
#import SUB_GNAR.AntennaCheck as AC
import SUB_GNAR.Menu as MN


def gnarMain():
    """ GNAR Application Main() function"""
    # mssqlConnection()
    # AC.MakeCSV(AC.antennaDecode)
    # AntAudit = AC.AntennaAudit() 
    # AntAudit.buildAntennaDF()
    # AntAudit.MakeCSV()
    # AntAudit.joinDF()
    # AntAudit.CleanDF()
    # AntAudit.AntennaChecksum()
    # MN.menuPrint()
    MN.getChoice()    
    # END OF MAIN FUNCTION
    
  
if __name__ == '__main__':

    gnarMain()
    print("THats all folks")

# END OF PY SCRIPT

