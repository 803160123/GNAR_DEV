######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240225
# Purpose: GNAR - General Netowork Audit and Remediation main function 
# Functions: menu print code
# Update: v0.1
# Notes:
######################################################################################

# from SUB_GNAR.ReportGNAR import logg
# import sys

# os.system('color') # NEED AN INTERACTIVE TERMINAL FOR THIS TO WORK (LINUX, POWERSHELL, MAC)

def menuPrintAll(): 
		# print('\n')  
		print('\t\t************************************************************************')
		print('\t\t**                                                                    **')
		print('\t\t**                  This is a private database utility.               **')
		print('\t\t**             All activity is subject to monitoring.                 **')
		print('\t\t**          Any UNAUTHORIZED access or use is PROHIBITED,             **')
		print('\t\t**                and may result in PROSECUTION.                      **')
		print('\t\t**                                                                    **')
		print('\t\t************************************************************************')
		print('\n')
		print('\t\t\t\t\t  ____ _   _    _    ____  ')
		print("\t\t\t\t\t / ___| \\ | |  / \\  |  _ \\") 
		print('\t\t\t\t\t| |  _|  \| | / _ \ | |_) |')
		print('\t\t\t\t\t| |_| | |\  |/ ___ \|  _ <') 
		print('\t\t\t\t\t \\____|_| \_/_/   \\_\\_| \\_\\')
		print('\n')
		print('\t\t\t  General Network Audit and Remediation By Chris Park')
		#print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
		print('====================================================================================================')
		print('\n')
		print('OPTION		DESCRIPTION			OPTION		DESCRIPTION')
		print('1		POWER SIMULATION DB -- AUDIT	2		POWER SIMULATION DB -- REMEDIATION')
		print('3		POWER NETWORK DB -- AUDIT	4		POWER NETWORK DB REMEDIATION')
		print('5		ANTENNA SIMULATION DB -- AUDIT	6		ANTENNA SIMULATION DB -- REMEDIATION')
		print('\n')
		print('\t\t\t\t\t q  QUIT')
		print('\n')
		print('====================================================================================================')

def menuPrint(): 
		print('\t\t\t\t\t  ____ _   _    _    ____  ')
		print("\t\t\t\t\t / ___| \\ | |  / \\  |  _ \\") 
		print('\t\t\t\t\t| |  _|  \| | / _ \ | |_) |')
		print('\t\t\t\t\t| |_| | |\  |/ ___ \|  _ <') 
		print('\t\t\t\t\t \\____|_| \_/_/   \\_\\_| \\_\\')
		print('\n')
		print('\t\t\t  General Network Audit and Remediation By Chris Park')
		#print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
		print('====================================================================================================')
		print('\n')
		print('OPTION		DESCRIPTION			OPTION		DESCRIPTION')
		print('1		POWER SIMULATION DB -- AUDIT	2		POWER SIMULATION DB -- REMEDIATION')
		print('3		POWER NETWORK DB -- AUDIT	4		POWER NETWORK DB REMEDIATION')
		print('5		ANTENNA SIMULATION DB -- AUDIT	6		ANTENNA SIMULATION DB -- REMEDIATION')
		print('\n')
		print('\t\t\t\t\t q  QUIT')
		print('\n')
		print('====================================================================================================')
        

'''
def getChoice() -> str:
	menuPrintAll()
	# option = int(input("PLEASE ENTER MENU OPTION TO EXECUTE: "))
	menu_options = {'1': 0, '2': 1, '3': 2, '4': 3, 'q': 4}
	# command_list = []	
    
	while True:
         user_input = str(input("PLEASE ENTER MENU OPTION TO EXECUTE>> "))
         user_input = user_input.strip()
         try:
             if user_input in menu_options:
                print(user_input)
                ### RIGHT HERE IS WHERE I WANT TO RETUNR  THE STRING VALUE BACK TO MAIN() ###
                if user_input == 'q':
                    print("THAT'S ALL FOLKS!")
                    logg.info("GNAR IS EXITING EXIT CODE 0")
                    break
                    # sys.exit(0)
                else:
                    # return user_input
                    input("PRESS ANY KEY TO CONTINUE>>")
                    menuPrint()
             else:
                 print(f"{user_input} IS NOT A VALID INPUT") 
                 # input("PRESS ANY KEY TO CONTINUE>>")
                 menuPrint()
         except Exception as err:
              print (f'\n{user_input} is not an acceptable option.')
              # print("VALUE ERROR: {0}".format(err))
              logg.error(f"INPUT ERROR: {err} {user_input} IS NOT A VALID SELECTION")
              menuPrint()
			  # sys.exit(1)
'''			

	
	