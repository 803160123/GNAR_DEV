######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240210
# Purpose: GNAR - General Netowork Audit and Remediation main function 
# Functions: main()
# Update: v0.1
# Notes:
######################################################################################


import SUB_GNAR.AntennaCheck as AC
from SUB_GNAR.AtollPower import AtollPower
import SUB_GNAR.NetworkPower as NETP
import SUB_GNAR.Menu as MN
import SUB_GNAR.ReportGNAR as REP


def gnarMain():
    """ GNAR Application Main() function"""
    # FIRST FUNCTION BUILDS A DAILY REPORTING REPO IN THE FOLDER OF USERS CHOICE
    REP.buildGnarDir()
    # mssqlConnection()
    # AC.MakeCSV(AC.antennaDecode)
    # AntAudit = AC.AntennaAudit() 
    # AntAudit.buildAntennaDF()
    # AntAudit.MakeCSV()
    # AntAudit.joinDF()
    # AntAudit.CleanDF()
    # AntAudit.AntennaChecksum()
    ### MENU TESTING ###
    # MN.menuPrint()
    # MN.getChoice()    
    #### CREATE NETWORK CLASS ####
    # PwrTest = NETP.NetworkPower()
    #### TEST NETWORK POWER OUTPUT FULL ####
    # PwrTest.updateNetworkPwr()
    ### TESTING METHODS
    # PwrTest.BuildNetPowerDF()
    # PwrTest.PwrSummary()
    
    #### SIMULATION DB TESTING ### 
    AtollAudit = AtollPower()
    # AtollAudit.BuildAtollPowerDF()
    AtollAudit.updateAtollParms()
        
    # END OF MAIN FUNCTION
 

  
if __name__ == '__main__':

    gnarMain()
    print("THats all folks")

# END OF PY SCRIPT

