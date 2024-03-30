######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240218
# Purpose: MSSQL CONNECTION <DBConnection.py>
# Functions: GNAR CONNECTTO MSSQL DB
# Update: 
######################################################################################

#import os
import sys
import pypyodbc as odbc
from SUB_GNAR.ReportGNAR import logg
  
def mssqlConnection():    
    """ function connects to local mssql GNAR_DEV database where network and simulation data is stored"""
    
    # SQL SERVERNAME NYCDTL01CP965X\SQLEXPRESS

    DRIVER_NAME = 'SQL SERVER'
    SERVER_NAME = 'NYCDTL01CP965X\SQLEXPRESS'
    DATABASE_NAME = 'GNAR_DEV'
        
    connection_string = f"""
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
    """
    try:
        conn = odbc.connect(connection_string)
        print(conn) # PRINTS THE ODBC CONNECTION STRING
        logg.info(f"CONN ESTABLISHED {conn}")
    except Exception as err:
        print(err)
        print('TEST CONNECTION IS BAD, CHECK THAT DATABASE IS RUNNING')
        logg.error(f"DB CONNECTION ERROR: {err} EXITING")
        sys.exit() 
    else:
        cursor = conn.cursor()
        # print('FIRE THAT QUERY UP')
        return cursor
       
    # END OF FUNCTION 

def closeCursor(cur):
    try:
        cur.close() #when we are done with the cursor.
    except Exception as err:
        print(err)
        print('NOT ABLE TO CLOSE TEST CONNECTION, SOMETHING WENT WRONG')
        logg.error(f"DB CONNECTION CLOSE ERROR: {err} EXITING")
        sys.exit() 
    else:
        print('<pypyodbc.Connection closed>') 
        logg.info("DB CONNECTION CLOSED")