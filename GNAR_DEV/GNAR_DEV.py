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
from SUB_GNAR.ReportGNAR import logg


def gnarMain() -> None:
    """ GNAR Application Main() function"""
    # FIRST FUNCTION BUILDS A DAILY REPORTING REPO IN THE FOLDER OF USERS CHOICE
    REP.buildGnarDir()
    logg.info('GNAR IS STARTING')
    # mssqlConnection()
    
    ### ANTENA AUDIT BUILD ###
    # AntAudit = AC.AntennaAudit() 
    # AntAudit.AntennaChecksum()
    # AntAudit.AntennaCorrect()


    ### ANTENNA METHOD TESTING ###
    # AC.MakeCSV(AC.antennaDecode)
    # AntAudit.buildAntennaDF()
    # AntAudit.MakeCSV()
    # AntAudit.joinDF()
    # AntAudit.CleanDF()
    
    ### MENU TESTING ###
    # MN.menuPrint()
    # MN.getChoice()    
        
    #### TEST NETWORK POWER OUTPUT FULL ####
    PwrTest = NETP.NetworkPower()
    PwrTest.updateNetworkPwr()
    
    ### TESTING NETWORK BUILD ###
    # PwrTest.BuildNetPowerDF()
    # PwrTest.PwrSummary()
    
    #### SIMULATION ATOLL DB BUILD ### 
    # AtollAudit = AtollPower()
    # AtollAudit.BuildAtollPowerDF()
    # AtollAudit.updateAtollParms()
        
    # END OF MAIN FUNCTION
 

  
if __name__ == '__main__':

    gnarMain()
    print("THats all folks")
    logg.info("GNAR IS EXITING EXIT CODE 0")

# END OF PY SCRIPT

