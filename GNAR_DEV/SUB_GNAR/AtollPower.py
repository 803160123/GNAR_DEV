######################################################################################
# Name: Chris Park
# Course: SDEV 435 Applied SW Practice I
# Date: 20240312
# Purpose: Network ATOLLPower Check Class
# Functions: GNAR ATOLL Power
# Update: v1
# NEED TO ADD ALL EXCEPTION HANDLING
######################################################################################


# import os
import sys
import datetime
import pandas as pd
# import numpy as np
# import tabulate
import SUB_GNAR.DBConnection as DB
import SUB_GNAR.ReportGNAR as REP
from SUB_GNAR.ReportGNAR import logg



           
class AtollPower():
    """ATOLL SIMULATION POWER CHECK AUDIT OBJECT THAT TAKES IN A QUERY THAT CONVERTS AND CLEANS DATA AND CREATES A DF TO CHECK POWER PARMS ARE CORRECT"""
    """ CHANGE THIS TO PASS IN THE SQL AS A PARAMETER """
    def __init__(self):
       print("Atoll Power Audit Constructor")
       self.atollSql = """
			WITH ATOLL AS(
				SELECT -- *
				A.PULLDATE,
				A.USID,
				-- A.SITE_NAME,
				A.ENODEB,
				A.EUTRANCELLFDD,
				A.STATUS,
				T.ACTIVE AS TX_ACTIVE,
				C.ACTIVE AS CL_ACTIVE,
				T.TX_ID,
				C.CELL_ID,
				-- C.CARRIER,
				A.ENM_NOOFTX,
				T.N_TX_ANTENNAS AS TX_N_TX_ANTENNAS,
				A.ENM_NOOFRX,
				T.N_RX_ANTENNAS AS TX_N_RX_ANTENNAS,
				T.N_TX_PA AS TX_N_TX_PA, 
				A.ENM_MAXTXPWR,
				(CASE WHEN A.FREQBAND = 30 THEN 44
				ELSE ROUND(A.ENM_REF_BRANCH_DBM,1) END) AS ENM_BRANCH_DBM,
				ROUND(C.MAX_POWER,1) AS CELL_MAX_POWER,
				--NEED TO ADD A CALC_MISCDL
				(CASE WHEN A.FREQBAND = 30 AND A.ENM_NOOFTX = 4 THEN (ROUND((49 - (LOG(A.ENM_MAXTXPWR,10)*10)),1)+1.5)
				WHEN A.FREQBAND = 30 AND A.ENM_NOOFTX = 2 THEN (ROUND((47 - (LOG(A.ENM_MAXTXPWR,10)*10)),1)+.5)
				ELSE ROUND(T.MISCDLL,2) END) AS CALC_MISCDLL,
				--
				ROUND(T.MISCDLL,2) AS MISCDLL,
				ROUND(CAST(A.ENM_CRSGAIN AS FLOAT),2) AS ENM_CRSGAIN,
				(CASE WHEN A.ENM_CRSGAIN = 0 THEN 1
				WHEN A.ENM_CRSGAIN = 3 THEN 2
				WHEN A.ENM_CRSGAIN = 6 THEN 4
				WHEN A.ENM_CRSGAIN = -3 THEN 1
				WHEN A.ENM_CRSGAIN = -1.77 THEN 1
				WHEN A.ENM_CRSGAIN = 1.77 THEN 2
				WHEN A.ENM_CRSGAIN = 4.77 THEN 4
				ELSE 0 END) AS ENM_CRSPORTS,
				C.N_CRS_PORTS,
				(CASE WHEN A.ENM_CRSGAIN = 0 THEN 0
				WHEN A.ENM_CRSGAIN = 3 THEN 0
				WHEN A.ENM_CRSGAIN = 6 THEN 0
				WHEN A.ENM_CRSGAIN = -3 THEN 3
				WHEN A.ENM_CRSGAIN = -1.77 THEN 1.77
				WHEN A.ENM_CRSGAIN = 1.77 THEN 1.5
				WHEN A.ENM_CRSGAIN = 4.77 THEN 1.5
				ELSE 0 END) AS ENM_PWR_OFFSET,	
				CAST(ISNULL(C.PBCH_POWER_OFFSET,0) AS FLOAT) AS PBCH_POWER_OFFSET
			--
			--
			FROM [GNAR_DEV].[dbo].[NETWORK_STATUS_20240226] A
			JOIN [dbo].[CELLS_ATOLLv1] C ON C.CELL_ID = A.EUTRANCELLFDD
			JOIN [dbo].[CELL_ID_ATOLLv1] ID ON ID.CELL_ID = C.CELL_ID
			JOIN [dbo].[TX_ATOLLv2] T ON T.TX_ID = ID.TX_ID
			WHERE 1=1 
			-- AND A.ENODEB = 'UNL05823'
			AND A.ENODEB LIKE 'UN%'
			AND A.USID = 61423 -- UNL00104
			-- AND A.USID = 115897 -- WEIBEL AVE
            -- AND A.USID IN (95345, 132292)
			-- AND A.FREQBAND IN (4,66,2,17,5,29,30)
			-- AND A.FREQBAND = 30
			-- AND A.ENM_CRSGAIN NOT IN (0,3,6)
			AND A.EUTRANCELLFDD NOT LIKE '%_DB'
			-- AND ROUND(A.ENM_REF_BRANCH_DBM,1) <> ROUND(C.MAX_POWER,1)
			-- AND (ROUND(A.ENM_REF_BRANCH_DBM,1) <> ROUND(C.MAX_POWER,1) OR A.ENM_NOOFTX <> T.N_TX_ANTENNAS)
			)
			------------------------------------------------------------------------------------
			SELECT 
			AT.*,
			(CASE WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) AND (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) AND (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX) AND (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'TX_BRANCH CL_PWR CL_CRSPORT TX_MISCDLL'
			WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) AND (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) AND (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX)  THEN 'TX_BRANCH CL_PWR CL_CRSPORT'
            WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) AND (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX) AND (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'TX_BRANCH CL_PWR TX_MISCDLL'
			WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) AND (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) AND (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'CL_PWR CL_CRSPORT TX_MISCDLL'
			WHEN (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) AND (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX) AND (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'TX_BRANCH CL_CRSPORT TX_MISCDLL'
			WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) AND (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX)  THEN 'TX_BRANCH CL_PWR'
            WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) AND (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) THEN 'CL_PWR CL_CRSPORT'
            WHEN (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) AND (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'CL_CRSPORT TX_MISCDLL'
            WHEN (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX) AND (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'TX_BRANCH TX_MISCDLL'
            WHEN (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX) AND (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) THEN 'TX_BRANCH CL_CRSPORT' --NEW
            WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) AND (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'CL_PWR TX_MISCDLL' --NEW
            WHEN (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER) THEN 'CL_PWR'
			WHEN (AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.ENM_PWR_OFFSET <> AT.PBCH_POWER_OFFSET) THEN 'CL_CRSPORT'
            WHEN (AT.CALC_MISCDLL <> AT.MISCDLL) THEN 'TX_MISCDLL'
            WHEN (AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX) THEN 'TX_BRANCH'
			ELSE NULL END) AS FLAG
			--
			FROM ATOLL AT
			WHERE 1=1
			-- AND AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX
			-- AND AT.N_CRS_PORTS <> AT.ENM_CRSPORTS
			-- AND AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER
			-- AND (AT.ENM_BRANCH_DBM <> AT.CELL_MAX_POWER OR AT.N_CRS_PORTS <> AT.ENM_CRSPORTS OR AT.TX_N_TX_ANTENNAS <> AT.ENM_NOOFTX)
			-- AND (AT.CALC_MISCDLL <> AT.MISCDLL)
			;
           """

       self.reportSql = """
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

    def BuildAtollPowerDF(self):
        """ THIS DF WILL BE USED FOR MULTIPLE SIMULATION TESTS AND REMEDIATION """
        curs = DB.mssqlConnection()
        curs.execute(self.atollSql)
        tempDf = curs.fetchall()
        atollDf = pd.DataFrame.from_records(tempDf, columns=[x[0] for x in curs.description])
        DB.closeCursor(curs)
        atollDf["STATUS"] = (atollDf["enm_branch_dbm"] == atollDf["cell_max_power"]) & (atollDf["n_crs_ports"] == atollDf["enm_crsports"]) \
            & (atollDf["enm_pwr_offset"] == atollDf["pbch_power_offset"]) & (atollDf["tx_n_tx_antennas"] == atollDf["enm_nooftx"]) & (atollDf["calc_miscdll"] == atollDf["miscdll"])
        # SEND ATOLL REPORT TO DIRECTORY 
        atollPath = REP.buildGnarFile('ATOLL')
        atollDf.to_csv(atollPath, index=False)
		# print(atollDf.to_markdown(tablefmt="grid"))  
        return atollDf

    def updateAtollParms(self):
        """ THIS METHOD IS RESPONSIBLE FOR TAKING THE FAILING ATOLL(SIMULATION) DATAFRAME VALUES AND UPDATING THE CORRECT TABLE TO REMEDIATE THE POWER IN THE SQL DB """
        aholeDf = self.BuildAtollPowerDF()
        print(aholeDf.to_markdown(tablefmt="grid"))
        sqlCommands = ""
        reportComm = self.reportSql
        cellTable = '[dbo].[CELLS_ATOLLv1]'
        txTable = '[dbo].[TX_ATOLLv2]'
        """ I NEED TO CHANGE THE BELOW SQL LOGIC AS IT IS NOT UPDATING ALL OF THE APPROPRIATE DISCREPANCIES, ONLY UPDING THE FIRST CHANGE BECAUSE OF THE IF/ELIF STATEMENT NEED TO REWRITE """
        for index, row in aholeDf.iterrows():
            # NEED TO REFACTOR THIS LOOP TO USE APPLY() w/ A LAMBDA IT CAN BE FASTER
            if (row["enm_branch_dbm"] != row["cell_max_power"]):
                sqlCommands += f"UPDATE {cellTable} SET MAX_POWER = {row['enm_branch_dbm']} WHERE CELL_ID = '{row['eutrancellfdd']}';\n"
                reportComm += f"(CURRENT_TIMESTAMP,'{row['pulldate']}','{cellTable}',{row['usid']},'{row['enodeb']}','{row['eutrancellfdd']}','cell_max_power','{row['cell_max_power']}','{row['enm_branch_dbm']}'),\n"
            elif (row["n_crs_ports"] != row["enm_crsports"]):
                sqlCommands += f"UPDATE {cellTable} SET N_CRS_PORT = {row['enm_crsports']} WHERE CELL_ID = '{row['eutrancellfdd']}';\n"
                reportComm += f"(CURRENT_TIMESTAMP,'{row['pulldate']}','{cellTable}',{row['usid']},'{row['enodeb']}','{row['eutrancellfdd']}','n_crs_port','{row['n_crs_ports']}','{row['enm_crsports']}'),\n"
            elif (row["enm_pwr_offset"] != row["pbch_power_offset"]):
                sqlCommands += f"UPDATE {cellTable} SET PBCH_POWER_OFFSET = {row['enm_pwr_offset']} WHERE CELL_ID = '{row['eutrancellfdd']}';\n"
                reportComm += f"(CURRENT_TIMESTAMP,'{row['pulldate']}','{cellTable}',{row['usid']},'{row['enodeb']}','{row['eutrancellfdd']}','pbch_power_offset','{row['pbch_power_offset']}','{row['enm_pwr_offset']}'),\n"
            elif (row["tx_n_tx_antennas"] != row["enm_nooftx"]):
                sqlCommands += f"UPDATE {txTable} SET N_TX_ANTENNAS = {row['enm_nooftx']}, N_RX_ANTENNAS = {row['enm_noofrx']} WHERE TX_ID = '{row['tx_id']}';\n"
                reportComm += f"(CURRENT_TIMESTAMP,'{row['pulldate']}','{txTable}',{row['usid']},'{row['enodeb']}','{row['eutrancellfdd']}','n_tx_antennas','{row['tx_n_tx_antennas']}','{row['enm_nooftx']}'),\n"
                reportComm += f"(CURRENT_TIMESTAMP,'{row['pulldate']}','{txTable}',{row['usid']},'{row['enodeb']}','{row['eutrancellfdd']}','n_rx_antennas','{row['tx_n_rx_antennas']}','{row['enm_noofrx']}'),\n"
            elif (row["calc_miscdll"] != row["miscdll"]):
                sqlCommands += f"UPDATE {txTable} SET MISCDLL = {row['calc_miscdll']} WHERE TX_ID = '{row['tx_id']}';\n"
                reportComm += f"(CURRENT_TIMESTAMP,'{row['pulldate']}','{txTable}',{row['usid']},'{row['enodeb']}','{row['eutrancellfdd']}','miscdll','{row['miscdll']}','{row['calc_miscdll']}'),\n"
        # NEED TO  TEST WHETHER THE updateQuery IS NULL BEFORE CONNECTING TO THE DB		
        # print(reportComm)
        
        if sqlCommands == "":
            print("THERE ARE NO ATOLL DATABASE DISCREPANCIES TO REMEDIATE, NICE JOB!")
        else:
            # PRINT STATEMENTS ARE JUST FOR SYNTAX TESTING COMMENT OUT FOR PRODUCTION
            # print(sqlCommands)
            reportComm = reportComm[:-2]+';'
            # print(reportComm)
            curs = DB.mssqlConnection()
            try:
                curs.execute(sqlCommands)
                curs.commit()
                # ADD A SUMMARY OF UPDATES HERE
                print('ATOLL UPDATES WERE COMMITED TO DATABASE')
                curs.execute(reportComm)
                curs.commit()
                print('GNAR REPORT UPDATES WERE COMMITED TO DATABASE')
            except Exception as err:
                print(err)
                print('SOMETHING WENT WRONG, THAT NETWORK SQL UPDATE DIDNT WORK')
                logg.error(f"DB ATOLL REPORT/ATOLL WRITE ERROR: {err} EXITING")
                sys.exit() 
			
            DB.closeCursor(curs)  
		
# END OF ATOLL POWER CLASS


                
        