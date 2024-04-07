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
import SUB_GNAR.ReportGNAR as REP
from SUB_GNAR.ReportGNAR import logg



class AntennaAudit():
    """ANTENNA CHECK AUDIT OBJECT THAT TAKES IN A QUERY AND A FLATFILE (ANTENNA DECODER) THAT CONVERTS AND CLEANS DATA AND CREATES A DF"""
    def __init__(self, decoder=None, antennaSql=None):
        print("AntennaCheck Constructor")
        self.antennaDecode = 'C:\\Users\\cp965x\\source\\repos\\GNAR_DEV\\GNAR_DEV\\SUB_GNAR\\ANTENNA_DECODEv2.csv'

        self.gnarAntennaPullSql = """ SELECT -- *
					A.PULLDATE,
					A.USID,
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
					-- AND A.USID = 60590 VA HOSPITAL
					AND A.USID = 95345
                    AND A.ENODEB LIKE 'UN%'
					AND A.FREQBAND IN (4,66,2,17,5,29,66)
					;	
                    """
        self.decoder = self.antennaDecode
        self.antennaSql = self.gnarAntennaPullSql
        self.antReportUpdateQ = """
                USE GNAR_DEV;
                INSERT INTO dbo.REPORT_HISTORY (
	            [DATETIME], 
	            [PULLDATE],
	            [GNAR_TABLE],
	            [USID],
	            [ENODEB], 
	            [EUTRANCELLFDD],
	            [PARAMETER],
	            [PRE],
	            [POST])
                VALUES
                """

    def BuildAntennaDF(self):
        """ THIS METHOD IS RESPONSIBLE FOR QUERYING THE SIMULATION AND NETWORK MSSQL DB AND RETURNING ALL APPLICABLE PARMS"""   
        curs = DB.mssqlConnection()
        curs.execute(self.gnarAntennaPullSql)
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
            antFile = pd.read_csv(self.antennaDecode)
            # print("CREATED A DF CALLED antFile")
			# FOR TESTING 
            # top5Lines = antFile.head()
            # print(top5Lines.to_markdown(tablefmt="grid"))
            return antFile
        except Exception as err:
            print("EXCEPTION ERROR: {0}".format(err))
            logg.error(f"VALUE ERROR:{err} Failed to convert csv to DF: Exiting")
            sys.exit(1)
        except ValueError as verr:
            print("VALUE ERROR: {0}".format(verr))
            logg.error(f"VALUE ERROR:{verr} Failed to convert csv to DF: Exiting")
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
        except Exception as err:
            print("EXCEPTION ERROR: {0}".format(err))
            logg.error(f"VALUE ERROR:{err} Failed to join dataframes: Exiting")
            sys.exit(1)
        except ValueError as verr:
            print("VALUE ERROR: {0}".format(verr))
            logg.error(f"VALUE ERROR: {verr} Failed to join dataframes: Exiting")
            sys.exit(1)
        except TypeError as terr:
            print("TYPE ERROR: {0}".format(terr))
            logg.error(f"TYPE ERROR:{terr} Failed to join dataframes: Exiting")
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
        """ THIS METHOD IS THE FINAL ANTENNA DF CHECK, WHICH PRODUCES THE RESULTS AND PRINT TO SCREEN """
        finalAntDf = self.CleanDF()
        finalAntDf["STATUS"] = finalAntDf["antenna_name"].str.strip() == finalAntDf["ENM_MODEL_DECODE"].str.strip()
        # COMMENT OUT THE BELOW FOR ALL DF COLUMNS
        finalAntDf = finalAntDf[["pulldate", "usid", "enodeb", "eutrancellfdd", "tx_id", "cell_id", "enm_antenna", "enm_antenna_etilt", "antenna_name", "enm_antmodel_key", "ENM_MODEL_DECODE", "STATUS"]]
        # SEND ANTENNA ATOLL REPORT TO DIRECTORY 
        antennaPath = REP.buildGnarFile('ANTENNA')
        finalAntDf.to_csv(antennaPath, index=False)
        # print(finalAntDf.to_markdown(tablefmt="grid")) 
        return finalAntDf
    
    def AntennaResults(self) ->None:
        reportAntDf = self.AntennaChecksum()
        shortFinalAntDf = reportAntDf[["pulldate","tx_id", "cell_id", "enm_antenna", "enm_antenna_etilt", "antenna_name", "enm_antmodel_key", "ENM_MODEL_DECODE", "STATUS"]]
        message5 = ['ANTENNA SIMULATION DB -- AUDIT']
        msg5Dict = {'OPTION 5': message5}    
        msg5Df = pd.DataFrame(msg5Dict)
        print(msg5Df.to_markdown(tablefmt="grid", index=False))
        print(shortFinalAntDf.to_markdown(tablefmt="grid")) 
        
    
    def AntennaCorrect(self):
        """ THIS METHOD WILL AGAIN OPEN A CONNECTION TO THE DATABASE AND UPDATE(WRITE) THE CORRECTIONS THAT ARE NEEDED AND LOG THOSE CORREXCTION """
        fixAntDf =  self.AntennaChecksum()
        antTableName = "[dbo].[TX_ATOLLv2]"
        antUpdateQuery = ""
        antReportBuilder = self.antReportUpdateQ
        
        for index, row in fixAntDf.iterrows():
            # NEED TO REFACTOR THIS LOOP TO USE APPLY() w/ A LAMBDA TO MAKE IT FASTER
            if row["STATUS"] == False: 
                antUpdateQuery += f"UPDATE {antTableName} SET ANTENNA_NAME = '{row['ENM_MODEL_DECODE']}' WHERE TX_ID = '{row['tx_id']}';\n"
                antReportBuilder += f"(CURRENT_TIMESTAMP,'{row['pulldate']}','{antTableName}',{row['usid']},'{row['enodeb']}','{row['eutrancellfdd']}','antenna_name','{row['antenna_name']}','{row['ENM_MODEL_DECODE']}'),\n"
         
        message6 = ['ANTENNA SIMULATION DB -- REMEDIATION']
        msg6Dict = {'OPTION 6': message6}    
        msg6Df = pd.DataFrame(msg6Dict)
        print(msg6Df.to_markdown(tablefmt="grid", index=False))        
        if antUpdateQuery == "":
            print("THERE ARE NO ATOLL ANTENNA DATABASE DISCREPANCIES TO REMEDIATE, NICE JOB!")
        else:
            shortFixAntDf = fixAntDf[["pulldate","tx_id", "cell_id", "enm_antenna", "enm_antenna_etilt", "antenna_name", "enm_antmodel_key", "ENM_MODEL_DECODE", "STATUS"]]
            print(shortFixAntDf.to_markdown(tablefmt="grid")) 
            # print(antUpdateQuery)
            antReportBuilder = antReportBuilder[:-2]+';'
            # print(antReportBuilder)
            curs = DB.mssqlConnection()
            try:
                curs.execute(antUpdateQuery)
                curs.commit()
                print('ATOLL ANTENNA UPDATES WERE COMMITTED TO THE DATABASE')
                curs.execute(antReportBuilder)
                curs.commit()
                print('GNAR REPORT UPDATES WERE COMMITED TO DATABASE')
            except Exception as err:
                print(err)
                print('SOMETHING WENT WRONG, THAT NETWORK SQL UPDATE DIDNT WORK')
                logg.error(f"EXCEPTION ERROR:{err} Failed to commit antenna changes to DB: Exiting")
                sys.exit(1) 
			
        DB.closeCursor(curs)  


    
    def ColumnsDf(self) -> None: 
        queryDf = self.buildAntennaDF()
        columns = queryDf.columns
        print("THE DF COLUMNS ARE:")
        for name in columns:
            print(name)
     
 
# END OF ANTENNA CHECK CLASS  
# END OF PY SCRIPT  