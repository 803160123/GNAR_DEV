######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240210
# Purpose: GNAR - General Netowork Audit and Remediation main function 
# Functions: gnar main()
# Update: v0.1
# Notes:
######################################################################################


import SUB_GNAR.AntennaCheck as AC
from SUB_GNAR.AtollPower import AtollPower
import SUB_GNAR.NetworkPower as NETP
import SUB_GNAR.Menu as MN
import SUB_GNAR.ReportGNAR as REP
from SUB_GNAR.ReportGNAR import logg
from SUB_GNAR.TxBuilder import builder


def gnarMain() -> None:
    """ GNAR Application Main() function"""
    # FIRST FUNCTION BUILDS A DAILY REPORTING REPO IN THE FOLDER OF USERS CHOICE
    REP.buildGnarDir()
    logg.info('GNAR IS STARTING')
    # mssqlConnection()
        
    # MAIN GNAR APPLICATION STARTS HERE
    
    def getChoice() -> None:
        MN.menuPrintAll()
	    # option = int(input("PLEASE ENTER MENU OPTION TO EXECUTE: "))
        menu_options = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, 'q': 7}
	    # command_list = []	
        
        while True:
             user_input = str(input("PLEASE ENTER MENU OPTION TO EXECUTE>> "))
             user_input = user_input.strip()
             try:
                 if user_input in menu_options:
                    print(user_input)
                    if user_input == 'q':
                        # print("THAT'S ALL FOLKS!")
                        logg.info("GNAR IS EXITING EXIT CODE 0")
                        break
                        # sys.exit(0)
                    elif user_input == '1':
                        AtollAudit = AtollPower()
                        AtollAudit.ReportAtollPower()
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                    elif user_input == '2':
                        AtollAudit2 = AtollPower()
                        AtollAudit2.updateAtollParms()
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                    elif user_input == '3':
                        PwrTest = NETP.NetworkPower()
                        PwrTest.ReportNetworkPwr()
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                    elif user_input == '4':
                        PwrTest2 = NETP.NetworkPower()
                        PwrTest2.updateNetworkPwr()
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                    elif user_input == '5':
                        AntAudit = AC.AntennaAudit() 
                        AntAudit.AntennaResults()
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                    elif user_input == '6':
                        AntAudit = AC.AntennaAudit() 
                        AntAudit.AntennaCorrect()
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                    elif user_input == '7':
                        builder()
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                    else:
                        # return user_input
                        input("PRESS ANY KEY TO CONTINUE>>")
                        MN.menuPrint()
                 else:
                     print(f"{user_input} IS NOT A VALID INPUT") 
                     # input("PRESS ANY KEY TO CONTINUE>>")
                     MN.menuPrint()
             except Exception as err:
                  print (f'\n{user_input} is not an acceptable option.')
                  # print("VALUE ERROR: {0}".format(err))
                  logg.error(f"INPUT ERROR: {err} {user_input} IS NOT A VALID SELECTION")
                  MN.menuPrint()
			      # sys.exit(1)
     
    getChoice()

    # HELPER METHODS BELOW FOR TESTING #

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
    # MN.menuPrintAll()
    # MN.getChoice()
            
    #### TEST NETWORK POWER OUTPUT FULL ####
    # PwrTest = NETP.NetworkPower()
    # PwrTest.updateNetworkPwr()
    
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
    print("THats all folks!!!")
    logg.info("GNAR IS EXITING EXIT CODE 0")

# END OF MAIN() PY SCRIPT

