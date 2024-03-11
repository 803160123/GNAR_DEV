######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240218
# Purpose: Antenna Check Class
# Functions: GNAR Antenna Audit Check
# Update: v1
# NOTE: NEED TO ADD LOGIC TO CATCH WHERE FLATFILE IS MISSING ANTENNA INFORMATION
# NEED TO ADD ALL EXCEPTION HANDLING
######################################################################################


# import os
import sys
# import datetime
import pandas as pd
# import numpy as np
# import tabulate
import SUB_GNAR.DBConnection as DB


antennaDecode = 'C:\\Users\\cp965x\\source\\repos\\GNAR_DEV\\GNAR_DEV\\SUB_GNAR\\ANTENNA_DECODEv2.csv'

gnarAntennaPullSql = """ SELECT -- *
					A.PULLDATE,
					-- A.SITE_NAME, -- OPTIONAL FOR TESTING
					A.ENODEB,
					A.EUTRANCELLFDD,
					T.TX_ID,
					C.CELL_ID,
					--
					A.ENM_ANTENNA,
					ROUND(A.ETILT,1) AS ENM_ANTENNA_ETILT,
					-- CAST(LTRIM(SUBSTR(SUBSTR(T.ANTENNA_NAME, -4, 4),1,2),'0') AS DECIMAL) AS ANT_TILT,
					-- TO_CHAR(ETILT,'00')||'DT') AS TEST_PAD
					RIGHT(100 + ROUND(A.ETILT,0), 2)+'DT' AS ANT_PAD,
					T.ANTENNA_NAME,
					A.ENM_NOOFTX,
					T.N_TX_ANTENNAS AS TX_N_TX_ANTENNAS,
					A.ENM_NOOFRX,
					T.N_RX_ANTENNAS AS TX_N_RX_ANTENNAS,
					T.N_TX_PA AS TX_N_TX_PA,
					UPPER(CASE WHEN A.ENM_ANTENNA IS NULL THEN NULL
					WHEN A.FREQBAND = 4 THEN A.ENM_ANTENNA+'_'+'66'
					WHEN A.FREQBAND = 29 THEN A.ENM_ANTENNA+'_'+'17'
					ELSE A.ENM_ANTENNA+'_'+CAST(A.FREQBAND AS nvarchar(5)) END)  AS ENM_ANTMODEL_KEY
					-- STATUS  IS MY LAST COLUMN TO HIGHLIGHT ISSUES
					--
					FROM [GNAR_DEV].[dbo].[NETWORK_STATUS_20240130] A
					JOIN [dbo].[CELLS_ATOLLv1] C ON C.CELL_ID = A.EUTRANCELLFDD
					JOIN [dbo].[CELL_ID_ATOLLv1] ID ON ID.CELL_ID = C.CELL_ID
					JOIN [dbo].[TX_ATOLLv2] T ON T.TX_ID = ID.TX_ID
					WHERE 1=1 
					-- AND A.ENODEB = 'UNL05823'
					AND A.USID = 60590
					AND A.ENODEB LIKE 'UN%'
					AND A.FREQBAND IN (4,66,2,17,5,29,66)
					;	
				"""


class AntennaAudit():
    """ANTENNA CHECK AUDIT OBJECT THAT TAKES IN A QUERY AND A FLATFILE (ANTENNA DECODER) THAT CONVERTS AND CLEANS DATA AND CREATES A DF"""
    def __init__(self, decoder=None, antennaSql=None):
        self.decoder = antennaDecode
        self.antennaSql = gnarAntennaPullSql
        print("AntennaCheck Constructor")

    def BuildAntennaDF(self):
        """ THIS METHOD IS RESPONSIBLE FOR QUERYING THE SIMULATION AND NETWORK MSSQL DB AND RETURNING ALL APPLICABLE PARMS"""   
        curs = DB.mssqlConnection()
        curs.execute(gnarAntennaPullSql)
        tempDf = curs.fetchall()
        antDf = pd.DataFrame.from_records(tempDf, columns=[x[0] for x in curs.description])
		# SQL TESTING
        # for row in curs:
        #    print(row)
		# cursor.commit()  #commits to the table
        DB.closeCursor(curs)
        # print(antDf.to_markdown(tablefmt="grid"))  
        return antDf
    

    def MakeCSV(self):
        """METHOD CONVERTS CSV FILE TO DATAFRAME"""
        try:
            antFile = pd.read_csv(antennaDecode)
            # print("CREATED A DF CALLED antFile")
			# FOR TESTING 
            # top5Lines = antFile.head()
            # print(top5Lines.to_markdown(tablefmt="grid"))
            return antFile
        except ValueError as verr:
            print("VALUE ERROR: {0}".format(verr))
			# NEED TO DEFINE MY LOGGING 
			# logging.error("TYPE ERROR: Failed to convert csv to DF: Exiting")
            sys.exit(1)
        except TypeError as terr:
            print("TYPE ERROR: {0}".format(terr))
			# NEED TO DEFINE MY LOGGING 
			# logging.error("TYPE ERROR: Failed to convert csv to DF: Exiting")
            sys.exit(1)

    def JoinDF(self):
        """ THIS METHOD CALLS THE csv AND sql METHODS AND DOES A LEFT JOIN ON THE 2 DATA SETS """
        decoderDf = self.MakeCSV()
        queryDf = self.BuildAntennaDF()
        # NEED TO ADD EXCEPTION HANDLING HERE:
        try:
            joinedDf = pd.merge(queryDf, decoderDf, on='enm_antmodel_key', how='left')
            # print(joinedDf.to_markdown(tablefmt="grid")) 
            return joinedDf
        except ValueError as verr:
            print("VALUE ERROR: {0}".format(verr))
			# NEED TO DEFINE MY LOGGING 
			# logging.error("TYPE ERROR: Failed to join dataframes: Exiting")
            sys.exit(1)
        except TypeError as terr:
            print("TYPE ERROR: {0}".format(terr))
			# NEED TO DEFINE MY LOGGING 
			# logging.error("TYPE ERROR: Failed to join dataframes: Exiting")
            sys.exit(1)
    
    def CleanDF(self):
        """ THIS METHOD CLEANS UP THE ANTENNA DECODE COLUMN AND JOINS THE BAND + MHZ + ANTENNA ELECTRICAL """ 
        cleanAntDf = self.JoinDF()
        # CONVERT BAND TO STR TYPE PRIOR TO BUILDING NEW COLUMN
        cleanAntDf["BAND"] = cleanAntDf["BAND"].astype(str).str.split('.', expand=True)[0]
        # COMBINE TO CREATE 
        cleanAntDf["ENM_MODEL_DECODE"] = cleanAntDf["ATOLL_MODEL_DECODE"] + '_' + cleanAntDf["BAND"] + cleanAntDf["MHZ"] + '_' + cleanAntDf["ant_pad"].str.strip()
        # print(cleanAntDf.to_markdown(tablefmt="grid")) 
        return cleanAntDf

    def AntennaChecksum(self):
        """ THIS METHOD IS THE FINAL ANTENA DF CHECK, WHICH PRODUCES THE RESULTS AND PRINT TO SCREEN """
        finalAntDf = self.CleanDF()
        finalAntDf["STATUS"] = finalAntDf["antenna_name"].str.strip() == finalAntDf["ENM_MODEL_DECODE"].str.strip()
        # COMMENT OUT THE BELOW FOR ALL DF COLUMNS
        finalAntDf = finalAntDf[["pulldate", "enodeb", "eutrancellfdd", "tx_id", "cell_id", "enm_antenna", "enm_antenna_etilt", "antenna_name", "enm_antmodel_key", "ENM_MODEL_DECODE", "STATUS"]]
        print(finalAntDf.to_markdown(tablefmt="grid")) 
        return finalAntDf
    
    def TestJoin(self):
        """ THIS METHOD WILL AGAIN OPEN A CONNECTION TO THE DATABASE AND UPDATE(WRITE) THE CORRECTIONS THAT ARE NEEDED AND LOG THOSE CORREXCTION """
        pass
    
    def ColumnsDf(self):
        queryDf = self.buildAntennaDF()
        columns = queryDf.columns
        print("THE DF COLUMNS ARE:")
        for name in columns:
            print(name)
     
        
        
 


# END OF ANTENNA CHECK CLASS  
# END OF PY SCRIPT  