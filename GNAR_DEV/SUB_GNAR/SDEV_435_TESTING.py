

import os
import sys
import datetime
#import pandas as pd
#import numpy as np
import pypyodbc as odbc

TODAY = datetime.datetime.now()
TIMESTAMP = TODAY.strftime('%y%m%d%H%M')
OUTPUT_FILE = 'ATOLL_UNY_TEST_'+TIMESTAMP+'.csv'
OUTPUT_FILE_CELL = 'ATOLL_UNY_CELL_'+TIMESTAMP+'.csv'

# SQL SERVERNAME NYCDTL01CP965X\SQLEXPRESS

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'NYCDTL01CP965X\SQLEXPRESS'
DATABASE_NAME = 'GNAR_DEV'

# Uid='cp965x';
# Pwd='Trucking01';

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
"""


try:
    conn = odbc.connect(connection_string)
    print(conn)
except Exception as e:
    print(e)
    print('TEST CONNECTION IS BAD')
    sys.exit() 
else:
    cursor = conn.cursor()
    print('FIRE THAT QUERY UP')

testSql = """SELECT * FROM [dbo].[NETWORK_STATUS_20240126] WHERE 1=1 AND USID = 301886; """

cursor.execute(testSql)

for row in cursor:
    print(row)


# cursor.commit()  #commits to the table
cursor.close() #when we are done with the cursor.

print('ALL DONE')

'''
try:
except Exception as e:
    
else:

finally:
    if conn.connected == 1:
        conn.close()
        print('CONNECTION CLOSED')
'''

