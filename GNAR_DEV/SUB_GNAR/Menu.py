######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240225
# Purpose: GNAR - General Netowork Audit and Remediation main function 
# Functions: menu code
# Update: v0.1
# Notes:
######################################################################################

# import os

# os.system('color')

def menuPrint(): 
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
		print('3		POWER NETWORK DB -- AUDIT	4		RESEREVED FOR NETWORK(FUTURE)')
		print('5		ANTENNA SIMULATION DB -- AUDIT	6		ANTENNA SIMULATION DB -- REMEDIATION')
		print('\n')
		print('\t\t\t\t\t q  QUIT')
		print('\n')
		print('====================================================================================================')
        


def getChoice():
	menuPrint()
	# option = int(input("PLEASE ENTER MENU OPTION TO EXECUTE: "))
	menu_options = {'1': 0, '2': 1, '3': 2, '4': 3, 'q': 4}
	command_list = [1]	

	while True:
		user_input = input("PLEASE ENTER MENU OPTION TO EXECUTE: ")
		try:
			if user_input in menu_options:
				print(user_input)
				break
			# if user_input in acceptable_options :
            # exec (command_list [acceptable_options [option]])	
			# FOR THIS I WOULD RETURN THE MENU OPTION AND HAVE A LIST IN MAIN THAT WOULD EXECUTE APPROPRIATE OPTION
		except ValueError as verr:
			print (f'\n{user_input} is not an acceptable option.')
			print("VALUE ERROR: {0}".format(verr))
			
'''		
display_menu = ((
    "[1] Search list of: ",
    "[2] Search a: ",
    "[3] No operation.",
    '[4] Go back to main page',
    "[0] Exit the program."),
    ('dummy_function ()',
    'dummy_function ()',
    'dummy_function ()',
    'operate_menu (main_menu)',
    'exit_the_program ()'))		
'''
		
	
	
	